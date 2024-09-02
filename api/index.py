from pywebio import start_server, config
from pywebio.input import *
from pywebio.output import *
import asyncio
from flask import Flask
from pywebio.platform.flask import webio_view
from pywebio.session import register_thread, run_js
from threading import Thread

app = Flask(__name__)
app.secret_key = "DOGZlsa1002fg"

PREMIUM_PASSWD = "lsa1002fg"
MAX_MSGS = 100

chat_msgs = []
online_users = []

@config(theme="dark", title="DOGZ")
def main():
	global chat_msgs
	run_js("$('head link[rel=icon]').attr('href', image_url)", image_url="https://w7.pngwing.com/pngs/555/167/png-transparent-air-airplane-logo-paper-plane-telegram-social-media-and-logos-icon.png")
	# dog = open("./imgs/dog.jpg", "rb").read()
	premium_star = "<img src=\"https://tgram.ru/blog/wp-content/uploads/2022/08/telegram_a2b79589744c739331\" alt=\"PREMIUM STAR\" width=\"10px\" height=\"10px\">"
	server_logo = '<img src="https://w7.pngwing.com/pngs/555/167/png-transparent-air-airplane-logo-paper-plane-telegram-social-media-and-logos-icon.png" alt="SERVER" width="25px" height="25px">'
	# put_image(dog)
	# put_image(premium_star, width="25px", height="25px")
	put_markdown("## Добро пожаловать в DOGZ!")
	msg_box = output()
	put_scrollable(msg_box, height=300, keep_bottom=True)

	name = input("Вход в чат", required=True, placeholder="Ваше имя", validate=lambda n: "Такое имя уже используется!" if n in online_users or n == ":D" else None)
	pd = input("Премиум пароль (необязательно)", required=False, placeholder="Пароль для получения премиум функций (необязательно)")
	user_logo = input("Ссылка на аватарку (необязательно)", required=False, placeholder="Ссылка")
	if user_logo:
		user_logo = f'<img src="{user_logo}" alt="USER LOGO" width="25px" height="25px">'
	else:
		user_logo = ""
	is_premium = True if pd == PREMIUM_PASSWD else False
	online_users.append(name)

	if is_premium:
		chat_msgs.append((":D", f"Присоединился пользователь {name} {premium_star}", False, server_logo))
		msg_box.append(put_html((f"{server_logo} <b>:D</b> : Присоединился пользователь {name} {premium_star}")))
	else:
		chat_msgs.append((":D", f"Присоединился пользователь {name}", False, server_logo))
		msg_box.append(put_html((f"{server_logo} <b>:D</b> : Присоединился пользователь {name}")))

	msger = Thread(target=refresh_msg, args=(name, msg_box))
	ref = register_thread(refresh_msg(name, msg_box))

	while True:
		data = input_group("Новое сообщение", [input(placeholder="Сообщение", name="msg"), actions(name="cmd", buttons=[">", {"label":"Выйти", "type":"cancel"}])], validate=lambda m: ('msg', "Введите текст сообщения!") if m["cmd"] == ">" and not m["msg"] else None)

		if data is None:
			break

		if is_premium:
			# msg_box.append(put_html(f"{name} {premium_star} : {data['msg']}"))
			# chat_msgs.append((name, data['msg'], is_premium))
			if data["msg"][0] == "!":
				cmd = data["msg"][1:]
				if cmd.split()[0] == "emoji":
					msg_box.append(put_html(f"{user_logo} <b>{name}</b> {premium_star} : <img src=\"{cmd.split()[1]}\" alt=\"EMOJI\" width=\"25px\" height=\"25px\">"))
					chat_msgs.append((name, data['msg'], is_premium, user_logo))
				elif cmd.split()[0] == "photo":
					msg_box.append(put_html(f"{user_logo} <b>{name}</b> {premium_star} : <img src=\"{cmd.split()[1]}\" alt=\"PHOTO\">"))
					chat_msgs.append((name, data['msg'], is_premium, user_logo))
				else:
					toast("Такой команды не существует")
			else:
				msg_box.append(put_html(f"{user_logo} <b>{name}</b> {premium_star} : {data['msg']}"))
				chat_msgs.append((name, data['msg'], is_premium, user_logo))
		else:
			msg_box.append(put_html(f"{user_logo} <b>{name}</b> : {data['msg']}"))
			chat_msgs.append((name, data['msg'], is_premium, user_logo))

	ref.close()
	online_users.remove(name)
	toast("Вы вышли")
	if is_premium:
		msg_box.append(put_html(f"{server_logo} <b>:D</b> : Пользователь {name} {premium_star} отключился"))
		chat_msgs.append((":D", f"Пользователь {name} {premium_star} отключился", False, server_logo))
	else:
		msg_box.append(put_html(f"{server_logo} <b>:D</b> : Пользователь {name} отключился"))
		chat_msgs.append((":D", f"Пользователь {name} отключился", False, server_logo))

async def refresh_msg(name, msg_box):
	global chat_msgs
	last_x = len(chat_msgs)
	premium_star = "<img src=\"https://frankfurt.apollo.olxcdn.com/v1/files/s59vk0nk2xfs1-UZ/image;s=600x0;q=50\" alt=\"PREMIUM STAR\" width=\"25px\" height=\"25px\">"
	server_logo = '<img src="https://w7.pngwing.com/pngs/555/167/png-transparent-air-airplane-logo-paper-plane-telegram-social-media-and-logos-icon.png" alt="SERVER" width="25px" height="25px">'
	while True:
		await asyncio.sleep(1)
		for m in chat_msgs[last_x:]:
			if m[0] != name:
				user_logo = m[3]
				if m[2]:
					if m[1][0] == "!":
						cmd = m[1][1:]
						if cmd.split()[0] == "emoji":
							msg_box.append(put_html(f"{user_logo} <b>{m[0]}</b> {premium_star} : <img src=\"{cmd.split()[1]}\" alt=\"PREMIUM STAR\" width=\"25px\" height=\"25px\">"))
						elif cmd.split()[0] == "photo":
							msg_box.append(put_html(f"{user_logo} <b>{m[0]}</b> {premium_star} : <img src=\"{cmd.split()[1]}\" alt=\"PHOTO\">"))
					else:
						msg_box.append(put_html(f"{user_logo} <b>{m[0]}</b> {premium_star} : {m[1]}"))
				else:
					msg_box.append(put_html(f"{user_logo} <b>{m[0]}</b> : {m[1]}"))

				# else:
		if len(chat_msgs) > MAX_MSGS:
			chat_msgs = chat_msgs[len(chat_msgs)//2:]
		last_x = len(chat_msgs)

app.add_url_rule("/", "webio_view", webio_view(main), methods=["GET", "POST"])

if __name__ == '__main__':
	# platform.path_deploy_http(".", port=8080, host="dogz.ru", cdn=False)
	# start_server(main, debug=True, port=8080, cdn=False)
	app.run(debug=False)