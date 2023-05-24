import bcrypt

passwd = bcrypt.hashpw('Solopagos1.'.encode(), bcrypt.gensalt()).decode()

print(passwd)
