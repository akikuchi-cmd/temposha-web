#!/bin/bash
# 株式会社テンポ社サイト — Xサーバー VPS へ公開する
#   使い方:  bash _deploy/deploy.sh          … サイトの中身だけ更新（ふだんはこれ）
#            bash _deploy/deploy.sh --setup  … 初回、または docker-compose.yml / nginx.conf を変えたとき
set -euo pipefail
cd "$(dirname "$0")/.."
HOST=xserver-vps
DIR=/opt/temposha

ssh $HOST "mkdir -p $DIR/site"
if [ "${1:-}" = "--setup" ]; then
  scp _deploy/docker-compose.yml _deploy/nginx.conf $HOST:$DIR/
fi

# 公開するファイルだけを送る（arcore.jp (1)/、app/、_deploy/、元画像の png などは載せない）
# --delete：サーバー側の site/ を手元の公開ファイルと完全に同じにする（/opt/temposha/site の中だけ）
rsync -az --delete --delete-excluded \
  --include='/index.html' --include='/company.html' --include='/service.html' \
  --include='/contact.html' --include='/gallery-content.html' \
  --include='/googleb674da6246a62dce.html' --include='/robots.txt' --include='/sitemap.xml' \
  --include='/style.css' --include='/script.js' --include='/logo.png' \
  --include='/favicon.ico' --include='/icon-192.png' --include='/icon-512.png' \
  --include='/apple-touch-icon.png' --include='/og-image.png' \
  --exclude='.DS_Store' --include='/images/***' \
  --exclude='*' \
  ./ $HOST:$DIR/site/

ssh $HOST "find $DIR/site -type d -exec chmod 755 {} + && find $DIR/site -type f -exec chmod 644 {} +"
if [ "${1:-}" = "--setup" ]; then
  ssh $HOST "cd $DIR && docker compose up -d"
fi
echo "公開しました → https://temposha.sys-app.jp/"
