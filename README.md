# fast_api
cd db
migration file 作成
alembic revision --autogenerate -m 'create users'
migration実行
alembic upgrade head
rollback 実行
alembic upgrade +1
alembic downgrade -1
alembic downgrade base