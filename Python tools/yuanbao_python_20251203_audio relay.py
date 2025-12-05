# audio_stream_server_simple.py
import pyaudio
import socket
import threading
import time
import json
import audioop
from collections import deque
import wave
import os

class AudioStreamServer:
    def __init__(self, host='0.0.0.0', port=5000, audio_format=pyaudio.paInt16, channels=2, rate=44100, chunk=1024):
        self.host = host
        self.port = port
        self.format = audio_format
        self.channels = channels
        self.rate = rate
        self.chunk = chunk
        self.audio = pyaudio.PyAudio()
        self.stream = None
        self.socket = None
        self.clients = []
        self.is_streaming = False
        self.volume_multiplier = 1.0
        
        # 音频处理参数
        self.sample_width = self.audio.get_sample_size(self.format)
        self.frame_buffer = deque(maxlen=10)  # 缓冲10个chunk
        
        print(f"音频流服务器初始化: {self.rate}Hz, {self.channels}通道, 块大小: {self.chunk}")

    def get_local_ip(self):
        """获取本地IP地址"""
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except:
            return "127.0.0.1"

    def start_server(self):
        """启动音频流服务器"""
        try:
            # 创建TCP服务器套接字
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.socket.bind((self.host, self.port))
            self.socket.listen(5)
            
            local_ip = self.get_local_ip()
            print(f"服务器启动在 {local_ip}:{self.port}")
            print("等待安卓客户端连接...")
            
            # 启动音频捕获
            self.start_audio_capture()
            
            # 接受客户端连接
            accept_thread = threading.Thread(target=self.accept_clients, daemon=True)
            accept_thread.start()
            
            # 启动控制台界面
            self.control_interface()
            
        except Exception as e:
            print(f"服务器启动失败: {e}")

    def start_audio_capture(self):
        """开始捕获系统音频"""
        try:
            # 查找可用的音频输入设备
            input_device = self.find_audio_input_device()
            
            self.stream = self.audio.open(
                format=self.format,
                channels=self.channels,
                rate=self.rate,
                input=True,
                frames_per_buffer=self.chunk,
                input_device_index=input_device,
                stream_callback=self.audio_callback
            )
            self.is_streaming = True
            self.stream.start_stream()
            print("音频捕获已启动")
        except Exception as e:
            print(f"音频捕获启动失败: {e}")

    def find_audio_input_device(self):
        """查找可用的音频输入设备"""
        print("可用的音频设备:")
        for i in range(self.audio.get_device_count()):
            dev_info = self.audio.get_device_info_by_index(i)
            if dev_info['maxInputChannels'] > 0:
                print(f"{i}: {dev_info['name']} (输入通道: {dev_info['maxInputChannels']})")
        
        # 尝试常见的环回设备名称
        loopback_keywords = ['stereo mix', '立体声混音', 'loopback', 'what you hear', 'virtual']
        for i in range(self.audio.get_device_count()):
            dev_info = self.audio.get_device_info_by_index(i)
            dev_name = dev_info['name'].lower()
            if any(keyword in dev_name for keyword in loopback_keywords) and dev_info['maxInputChannels'] > 0:
                print(f"找到环回设备: {dev_info['name']}")
                return i
        
        print("使用默认输入设备")
        return None

    def audio_callback(self, in_data, frame_count, time_info, status):
        """音频数据回调函数"""
        if self.is_streaming and in_data:
            # 音量调整 (移除了numpy依赖)
            if self.volume_multiplier != 1.0:
                try:
                    in_data = audioop.mul(in_data, self.sample_width, self.volume_multiplier)
                except:
                    pass  # 如果audioop失败，使用原始数据
            
            # 添加到缓冲区
            self.frame_buffer.append(in_data)
            
            # 发送给所有客户端
            self.broadcast_audio(in_data)
        
        return (in_data, pyaudio.paContinue)

    def broadcast_audio(self, audio_data):
        """广播音频数据给所有客户端"""
        disconnected_clients = []
        
        for client in self.clients:
            try:
                # 发送音频数据长度前缀
                data_len = len(audio_data)
                header = data_len.to_bytes(4, byteorder='big')
                client.send(header + audio_data)
            except (socket.error, BrokenPipeError):
                disconnected_clients.append(client)
        
        # 移除断开连接的客户端
        for client in disconnected_clients:
            self.clients.remove(client)
            print(f"客户端断开连接，当前客户端数: {len(self.clients)}")

    def accept_clients(self):
        """接受客户端连接"""
        while True:
            try:
                client_socket, addr = self.socket.accept()
                print(f"新客户端连接: {addr}")
                
                # 设置socket超时
                client_socket.settimeout(10.0)
                
                # 发送音频参数
                params = {
                    'rate': self.rate,
                    'channels': self.channels,
                    'format': self.format,
                    'chunk': self.chunk
                }
                param_str = json.dumps(params) + '\n'
                client_socket.send(param_str.encode())
                
                self.clients.append(client_socket)
                print(f"客户端已添加，当前客户端数: {len(self.clients)}")
                
                # 为每个客户端启动单独的发送线程
                client_thread = threading.Thread(target=self.handle_client, args=(client_socket,), daemon=True)
                client_thread.start()
                
            except Exception as e:
                print(f"接受客户端连接错误: {e}")

    def handle_client(self, client_socket):
        """处理单个客户端连接"""
        try:
            while True:
                # 发送缓冲区的音频数据
                for frame in list(self.frame_buffer):
                    try:
                        data_len = len(frame)
                        header = data_len.to_bytes(4, byteorder='big')
                        client_socket.send(header + frame)
                    except:
                        break
                time.sleep(0.1)  # 避免过于频繁的发送
        except:
            pass
        finally:
            if client_socket in self.clients:
                self.clients.remove(client_socket)
                print("客户端处理线程结束")

    def control_interface(self):
        """控制台界面"""
        while True:
            try:
                print("\n=== 音频流服务器控制台 ===")
                print("1. 查看状态")
                print("2. 调整音量")
                print("3. 列出音频设备")
                print("4. 退出")
                
                choice = input("请选择操作: ").strip()
                
                if choice == '1':
                    self.show_status()
                elif choice == '2':
                    self.adjust_volume()
                elif choice == '3':
                    self.list_audio_devices()
                elif choice == '4':
                    self.cleanup()
                    break
                else:
                    print("无效选择")
                    
            except KeyboardInterrupt:
                self.cleanup()
                break
            except Exception as e:
                print(f"控制台错误: {e}")

    def show_status(self):
        """显示服务器状态"""
        print(f"\n服务器状态:")
        print(f"IP地址: {self.get_local_ip()}:{self.port}")
        print(f"客户端数量: {len(self.clients)}")
        print(f"音频采样率: {self.rate}Hz")
        print(f"音频通道: {self.channels}")
        print(f"音量倍数: {self.volume_multiplier}")
        print(f"流状态: {'运行中' if self.is_streaming else '已停止'}")

    def list_audio_devices(self):
        """列出所有音频设备"""
        print("\n音频设备列表:")
        for i in range(self.audio.get_device_count()):
            dev_info = self.audio.get_device_info_by_index(i)
            print(f"{i}: {dev_info['name']}")
            print(f"   输入通道: {dev_info['maxInputChannels']}, 输出通道: {dev_info['maxOutputChannels']}")

    def adjust_volume(self):
        """调整音量"""
        try:
            vol = float(input("请输入音量倍数 (0.1-5.0): "))
            if 0.1 <= vol <= 5.0:
                self.volume_multiplier = vol
                print(f"音量已设置为: {vol}")
            else:
                print("音量范围应为0.1-5.0")
        except ValueError:
            print("请输入有效数字")

    def cleanup(self):
        """清理资源"""
        print("正在关闭服务器...")
        self.is_streaming = False
        
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
        
        if self.audio:
            self.audio.terminate()
        
        for client in self.clients:
            try:
                client.close()
            except:
                pass
        
        if self.socket:
            self.socket.close()
        
        print("服务器已关闭")

if __name__ == "__main__":
    # 检查pyaudio是否安装
    try:
        import pyaudio
    except ImportError:
        print("请先安装pyaudio: pip install pyaudio")
        print("如果安装失败，可以尝试: pip install pipwin 然后 pipwin install pyaudio")
        exit(1)
    
    # 创建并启动服务器
    server = AudioStreamServer(port=5000)
    
    try:
        server.start_server()
    except KeyboardInterrupt:
        server.cleanup()
    except Exception as e:
        print(f"服务器错误: {e}")
        server.cleanup()