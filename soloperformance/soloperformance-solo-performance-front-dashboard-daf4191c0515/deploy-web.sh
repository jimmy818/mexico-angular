# Configurar previamente el profile si no se tiene
# aws configure --profile=webdev
#set AWS_DEFAULT_PROFILE=webdev

# Compilar proyecto web/dashboard
ng build web --prod

# Publicar al bucket de AWS
aws s3 cp ./dist/web s3://dashboard.dev.soloperformance.app --profile webdev --recursive --acl public-read

# URL sitio
# d234k1yhp8us7e.cloudfront.net