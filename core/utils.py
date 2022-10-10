import base64


def retornaData(assinatura):
    ac = assinatura.split(',')
    acConvertida = ac[1]
    encoded_data = acConvertida

    decoded_data=base64.b64decode((encoded_data))

    return decoded_data
    

def saveMedia(assinatura, identidade):
        nome = str(identidade)
        print(nome)
        local = 'media/'
        ext = '.png'
        url = local+nome+ext

        img_file = open(url, 'wb')
        img_file.write(assinatura)
        img_file.close()

        return url
