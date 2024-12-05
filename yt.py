import subprocess
import json

def extract_m3u8_with_ytdlp(youtube_url):
    try:
        # 使用 yt-dlp 提取视频格式信息
        command = ["yt-dlp", "--dump-json", youtube_url]
        result = subprocess.run(command, capture_output=True, text=True)

        # 检查命令是否执行成功
        if result.returncode != 0:
            print(f"yt-dlp 错误: {result.stderr}")
            return None

        # 解析 yt-dlp 输出的 JSON 数据
        video_info = json.loads(result.stdout)

        # 打印视频信息以调试
        print(json.dumps(video_info, indent=4))  # 查看详细输出

        # 查找 .m3u8 格式的链接
        m3u8_url = None
        for fmt in video_info.get("formats", []):
            if fmt.get("protocol") == "m3u8_native":
                # 选择 URL 字段
                m3u8_url = fmt.get("url")
                print("找到的 .m3u8 流链接:", m3u8_url)
                break

        if not m3u8_url:
            print("未找到 .m3u8 流链接。")

        return m3u8_url
    except Exception as e:
        print("发生错误:", e)
        return None

def generate_m3u_playlist(m3u8_url, output_file="playlist.m3u"):
    try:
        if not m3u8_url:
            print("无效的 .m3u8 链接，无法生成播放列表。")
            return

        # 创建 M3U 播放列表文件
        m3u_content = f"#EXTM3U\n#EXTINF:-1,YouTube Live Stream\n{m3u8_url}\n"
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(m3u_content)

        print(f"M3U 播放列表文件已生成: {output_file}")
    except Exception as e:
        print("生成 M3U 播放列表时发生错误:", e)

if __name__ == "__main__":
    # 输入 YouTube 直播视频的 URL
    youtube_url = "https://www.youtube.com/watch?v=vr3XyVCR4T0"

    # 提取 .m3u8 流链接
    m3u8_url = extract_m3u8_with_ytdlp(youtube_url)

    # 如果找到 .m3u8 链接，生成播放列表
    if m3u8_url:
        generate_m3u_playlist(m3u8_url)
