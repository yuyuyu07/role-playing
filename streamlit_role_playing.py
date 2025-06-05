import streamlit as st  # 导入Streamlit库，用于创建Web应用界面
from openai_role_playing import get_gemini_response  # 从我们创建的 openai_对话.py 文件中导入函数
import os

# --- 侧边栏 ---
with st.sidebar:  # 侧边栏 布局
    st_api_key = st.text_input("请输入API密钥:", type="password")  # 密码 输入框 # 返回 文字
    st.markdown("[API获取地址](https://ai.google.dev/gemini-api/docs?hl=zh-cn)")
    st.markdown("---")

    # +------------------------------------------------------------------+
    # |                            角色扮演                               |
    # +------------------------------------------------------------------+
    file_path = st.text_input(  # 返回 文字
        "请输入角色文件:",  # 输入框的标签
        )  # 用户打开应用时，输入框里会预先显示这个值。
    if not file_path:  # 如果 点击按钮 并没有 输入 AIP密钥
        st.info("请输入角色文件")  # 提醒 提示
        st.stop()  # 终止 # 类似break

    f = open(file_path, "r", encoding="utf-8")    # open(文件路径，模式,编码方式)
    系统= f.read()

    st.text(f"{os.path.basename(file_path)}")  # 显示文件名

    # +------------------------------------------------------------------+
    # |                            清除聊天记录按钮                         |
    # +------------------------------------------------------------------+
    # 清除聊天记录按钮
    if st.button("清除聊天记录"):
        st.session_state["messages"] = [{"role": "system", "content": 系统}]
        st.rerun()  # 重新运行应用以更新界面

# --- 应用标题 ---
st.title("💬 Gemini 角色扮演")  # 设置网页应用的标题

# +------------------------------------------------------------------+
# |                             提交前 检查                            |
# +------------------------------------------------------------------+
# 检测api_key是否输入:
if not st_api_key:  # 如果 点击按钮 并没有 输入 AIP密钥
    st.info("请输入API密钥")  # 提醒 提示
    st.stop()               # 终止 # 类似break

# +------------------------------------------------------------------+
# |                            创建 显示消息（会话状态）                  |
# +------------------------------------------------------------------+
# 创建 欢迎介绍（会话状态）
# if 系统 is None:
# # 检测api_key是否输入:
# # if st_按钮 and not st_api_key:  # 如果 点击按钮 并没有 输入 AIP密钥
#     st.info("请输入API密钥")  # 提醒 提示
#     st.stop()               # 终止 # 类似break
if "messages" not in st.session_state:                   # 检查会话状态中是否存在 "messages" 键
    # "messages"变量名 和 记忆里的 messages=[]变量名 一致
    st.session_state["messages"] = [{"role": "system", "content": 系统}]

# +------------------------------------------------------------------+
# |                            显示 所有聊天消息                        |
# +------------------------------------------------------------------+
# for循环遍历会话状态中的所有消息，.chat_message方法 用并将它们显示在聊天界面上
for i in st.session_state["messages"]:              # 遍历 "st.session_state.messages" 列表中的每一条消息
    # 使用 st.chat_message 显示消息，
    if i["role"] != "system":  # !!! 关键改动：如果消息的角色不是 "system"，才显示它
        st.chat_message(i["role"]).write(i["content"])  # 消息的角色（"user" 或 "assistant"）决定了消息的显示样式，并使用 st.write 显示消息内容

# +------------------------------------------------------------------+
# |                            获取用户输入                            |
# +------------------------------------------------------------------+
# 将文本输入和提交按钮放在历史消息之后（默认在最低端）
prompt = st.chat_input("输入聊天消息")  # 聊天 输入框  # 不填为英文"Your message"

# +------------------------------------------------------------------+
# |                            处理用户输入                            |
# +------------------------------------------------------------------+
if prompt:  # 检查用户是否输入了内容
    # +------------------------------------------------------------------+
    # |                         将用户消息添加到历史中                       |
    # +------------------------------------------------------------------+
    # 将用户消息 添加到会话状态  ".append()列表添加方式" 将字典看作一个元素添加到列表中
    st.session_state["messages"].append({"role": "user", "content": prompt})  # 将用户消息添加到会话状态的 "messages" 列表中
    # 显示 用户聊天信息
    st.chat_message("user").write(prompt)  # 在聊天界面上显示用户消息

    # +------------------------------------------------------------------+
    # |                           记忆（历史消息列表）                       |
    # +------------------------------------------------------------------+
    # 2. 准备发送给API的聊天历史 (当前所有消息)
    messages_history = st.session_state["messages"]

    # +------------------------------------------------------------------+
    # |                             获得AI消息                             |
    # +------------------------------------------------------------------+
    with st.spinner("AI 正在思考中..."):  # 显示加载提示
        # 调用 get_gemini_response 函数
        response = get_gemini_response(st_api_key,messages_history)  # 传入当前的聊天历史

    # +------------------------------------------------------------------+
    # |                          将AI消息添加到历史中                        |
    # +------------------------------------------------------------------+
    # 将AI内容 添加到会话状态 ".append()列表添加方式" 将字典看作一个元素添加到列表中
    st.session_state["messages"].append({"role": "assistant", "content": response["content"]})  # 将 AI 助手的消息添加到会话状态的 "messages" 列表中
    # 显示 AI内容
    st.chat_message("assistant").write(response["content"])  # 在聊天界面上显示 AI 助手的消息

# streamlit run "E:\Code Project\python-project\role-playing\streamlit_role_playing.py"