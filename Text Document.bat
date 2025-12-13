
# 2. Инициализируйте Git (в корне, а не в папке api!)
git init

# 3. Добавьте все файлы
git add .

# 4. Сделайте первый коммит
git commit -m "API UUID"

# 5. Переименуйте ветку в main
git branch -M main

# 6. Свяжите с GitHub
git remote add origin https://github.com/gfdhdbdhfh-prog/uuid-api.git

# 7. Отправьте на GitHub
git push -u origin main   # ← вот здесь была ошибка: было "mai", нужно "main"