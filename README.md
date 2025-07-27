# 那我问你

## 安装

### 1. 安装Python环境
- **MacOS**:
  1. 打开终端。
  2. 运行以下命令安装Homebrew（如果尚未安装）：
     ```bash
     /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
     ```
  3. 安装Python 3：
     ```bash
     brew install python3
     ```
  4. 验证安装：
     ```bash
     python3 --version
     pip3 --version
     ```

- **Windows**:
  1. 访问 [Python官网](https://www.python.org/downloads/) 下载最新版本的Python 3。
  2. 运行安装程序，勾选 **"Add Python to PATH"** 选项。
  3. 完成安装后，打开命令提示符，验证安装：
     ```cmd
     python --version
     pip --version
     ```
  4. 进入安装目录，将python文件复制一份，重命名为python3。

### 2. 创建虚拟环境
1. 打开终端或命令提示符。
2. 导航到你的文档目录（MacOS/Linux）：
   ```bash
   cd ~/Documents
   ```
   Windows：
   ```cmd
   cd %USERPROFILE%\Documents
   ```
3. 创建并进入`python`目录：
   ```bash
   mkdir python && cd python
   ```
4. 创建虚拟环境：
   ```bash
   python3 -m venv venv
   ```
   Windows：
   ```cmd
   python -m venv venv
   ```
5. 激活虚拟环境：
   - MacOS/Linux：
     ```bash
     source venv/bin/activate
     ```
   - Windows：
     ```cmd
     venv\Scripts\activate
     ```

### 3. 安装依赖库
1. 在虚拟环境中，安装`openai`库：
   ```bash
   pip install openai
   ```

### 4. 克隆存储库
1. 克隆存储库到本地：
   ```bash
   git clone https://github.com/WilliamGao1130/LetMeAskYou.git
   ```
2. 进入项目目录：
   ```bash
   cd LetMeAskYou
   ```

### 5. 配置系统PATH
1. 将项目目录添加到系统PATH：
   - MacOS/Linux：
     编辑`~/.zshrc`或`~/.bashrc`文件，添加以下行：
     ```bash
     export PATH=$PATH:/path/to/LetMeAskYou
     ```
     然后运行：
     ```bash
     source ~/.zshrc
     ```
   - Windows：
     在系统环境变量中添加项目目录的`LetMeAskYou`文件夹路径。

### 6. 设置API密钥
1. 设置环境变量`DEEPSEEK-API-KEY`：
   - MacOS/Linux：
     ```bash
     export DEEPSEEK-API-KEY="your-api-key"
     ```
   - Windows：
     ```cmd
     set DEEPSEEK-API-KEY=your-api-key
     ```

大功告成！

## 使用

- 可以在命令行中使用`那我问你`跟随问题或`ask-ai`来使用。