import sys
import os
from twocaptcha import TwoCaptcha

# Verificar se a URL foi fornecida como argumento
if len(sys.argv) != 2:
    print("Uso: python3 solve_captcha.py <URL>")
    sys.exit(1)

url = sys.argv[1]

api_key = os.getenv('APIKEY_2CAPTCHA', 'c8ab907145f755a6f1f258e06531991d')

solver = TwoCaptcha(api_key)

try:
    result = solver.recaptcha(
        sitekey='6LfD3PIbAAAAAJs_eEHvoOl75_83eXSqpPSRFJ_u',  # Atualize conforme necessário
        url=url
    )
    recaptcha_token = result['code']
    print(recaptcha_token)  # Retorna o token do CAPTCHA
    
    

except Exception as e:
    print(f"Erro ao resolver CAPTCHA: {str(e)}")
    sys.exit(1)
