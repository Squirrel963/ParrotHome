import streamlit as st
import requests
import uuid

def verify_turnstile(response):
    # 替换为你的秘密密钥
    secret = '你的秘密密钥'
    url = 'https://challenges.cloudflare.com/turnstile/v0/siteverify'
    payload = {
        'secret': secret,
        'response': response
    }
    response = requests.post(url, data=payload)
    return response.json().get('success', False)

st.title('Streamlit + Cloudflare Turnstile Demo')

# 生成唯一的标识符，用于标识不同的用户会话
session_id = str(uuid.uuid4())

tur_keys = st.secrets["turnstile"]["api_key"]
# 嵌入 Cloudflare Turnstile 验证码
with st.container():
    st.components.v1.html(f'''
        <html>
        <head>
            <script src="https://challenges.cloudflare.com/turnstile/v0/api.js?onload=onLoad"></script>
        </head>
        <body>
            <div id="turnstile-container"></div>
            <script>
                window.onload = function() {{
                    var turnstileWidget = null;
                    window.onLoad = function() {{
                        turnstileWidget = turnstile.render(
                            '#turnstile-container', {{
                                sitekey: '{tur_keys}', // 替换为你的站点密钥
                                theme: 'light',
                                callback: function(response) {{
                                    // 验证成功后的回调函数
                                    console.log('Turnstile verification successful:', response);
                                    // 可以在这里记录验证码的响应结果，以便提交到服务器端进行验证
                                    window.streamlit.setComponentValue(response);
                                }},
                                error: function(error) {{
                                    console.error('Turnstile verification failed:', error);
                                }}
                            }}
                        );
                    }};

                    // 重新渲染 Turnstile 验证码
                    window.addEventListener('streamlit-reload', function() {{
                        if (turnstileWidget) {{
                            turnstileWidget.reset();
                        }}
                    }});
                }};
            </script>
        </body>
        </html>
    ''', height=100)

# 获取验证码的响应结果
turnstile_response = st.session_state.get('turnstile_response')

# 处理表单提交
if st.button('提交'):
    if turnstile_response:
        verification_result = verify_turnstile(turnstile_response)
        if verification_result:
            st.success('验证成功！')
            # 在这里可以添加其他业务逻辑
        else:
            st.error('验证失败，请重试。')
    else:
        st.error('请完成验证码验证。')