import subprocess

def run_yt_dlp(command):
    """运行 yt-dlp 命令并返回结果"""
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"运行命令出错: {e}")
        return None

def get_best_m3u8_link(youtube_url):
    """获取最佳 .m3u8 链接"""
    # 先运行 yt-dlp -F 获取视频格式
    print(f"获取视频格式信息: yt-dlp -F {youtube_url}")
    command = ["yt-dlp", "-F", youtube_url]
    format_info = run_yt_dlp(command)
    if format_info is None:
        return None

    print("视频格式信息已获取，正在获取最佳 .m3u8 链接...")

    # 然后运行 yt-dlp -f best --get-url 获取最佳 .m3u8 链接
    command = ["yt-dlp", "-f", "best", "--get-url", youtube_url]
    m3u8_url = run_yt_dlp(command)
    if m3u8_url is None:
        return None
    
    # 去除多余的空格和换行符
    m3u8_url = m3u8_url.strip()
    print(f"找到的 .m3u8 链接: {m3u8_url}")
    return m3u8_url

def save_m3u8_url(m3u8_url, filename="zt.m3u8"):
    """将 .m3u8 链接保存到文件"""
    try:
        with open(filename, "w", encoding="utf-8") as f:
            f.write(m3u8_url)
        print(f"已将 .m3u8 链接保存到 {filename}")
    except Exception as e:
        print(f"保存 .m3u8 链接时出错: {e}")

if __name__ == "__main__":
    youtube_url = "https://www.youtube.com/watch?v=vr3XyVCR4T0"  # 替换为你的 YouTube 视频链接
    m3u8_url = get_best_m3u8_link(youtube_url)
    
    if m3u8_url:
        save_m3u8_url(m3u8_url)
