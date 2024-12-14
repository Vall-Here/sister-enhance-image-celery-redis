# Run

1. buat terminal baru run "redis-server --bind 0.0.0.0"
2. buat terminal baru run python app.py
3. buat terminal baru run celery -A tasks flower
4. buat terminal baru run celery tasks.celery_app worker --loglevel=info
5. download postman
6. kirim postman dengan format form-data ke endpoint localhost\enhance-image dengan method post
7. untuk melihat hasil, kirim method get task dengan id


# ini masih percobaan 1 device, coba buat 2 device kalau bisa, fork repo ini 
