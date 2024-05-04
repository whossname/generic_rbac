if [$# -ne 1]; then
    echo -e "Expected one argument: migration name"
    exit
fi

source venv/bin/activate
pip install -r requirements/migrations.txt
alembic revision --autogenerate -m $1
