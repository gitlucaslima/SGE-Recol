import base64
from django.core.signing import TimestampSigner


def retornaData(assinatura):
    ac = assinatura.split(',')
    acConvertida = ac[1]
    encoded_data = acConvertida

    decoded_data = base64.b64decode((encoded_data))

    return decoded_data


def saveMedia(assinatura, identidade):

    local = 'media/assinaturas/'

    # Gerar um hash de
    signer = TimestampSigner()
    value = signer.sign(identidade).split(":")[-1]

    ext = '.png'
    url = local+'assinatura'+value+ext

    img_file = open(url, 'wb')
    img_file.write(assinatura)
    img_file.close()

    urlAlterada = url.split("/", 1)[1]

    return urlAlterada
