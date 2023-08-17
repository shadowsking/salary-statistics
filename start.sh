if [ ! -d "venv" ]; then
    source install.sh
fi

source venv/scripts/activate
python ./main.py
read -p "Press 'Enter' key to finish..."
