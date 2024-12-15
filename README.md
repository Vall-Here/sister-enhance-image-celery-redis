# Run

1. Hidupkan Virtual env python
2. buat terminal baru run "redis-server --bind 0.0.0.0"
3. buat terminal baru run python app.py
4. buat terminal baru run celery -A tasks flower
5. buat terminal baru run celery tasks.celery_app worker --loglevel=info -P eventlet atau celery tasks.celery_app worker --loglevel=info -P gevent
6. download postman
7. kirim postman dengan format form-data ke endpoint localhost\enhance-image dengan method post
8. untuk melihat hasil, kirim method get task dengan id


# ini masih percobaan 1 device, coba buat 2 device kalau bisa, fork repo ini 
