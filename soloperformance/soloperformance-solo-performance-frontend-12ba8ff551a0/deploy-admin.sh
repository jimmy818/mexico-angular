# Configurar previamente el profile si no se tiene
# aws configure --profile=admindev
#set AWS_DEFAULT_PROFILE=admindev

# Compilar proyecto admin
ng build admin --prod

# Publicar al bucket de AWS
aws s3 cp ./dist/admin s3://admin.dev.soloperformance.app --profile admindev --recursive --acl public-read

# URL sitio
# d234k1yhp8us7e.cloudfront.net