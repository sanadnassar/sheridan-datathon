from app import create_app

app = create_app()
client = app.test_client()

addresses = [
    "10 Downing St, London",
    "221B Baker St, London"
]

for addr in addresses:
    print(f"Posting address: {addr}")
    resp = client.post('/api/geocode', json={'address': addr})
    print('Status code:', resp.status_code)
    try:
        data = resp.get_json()
        print('Response:', data)
    except Exception:
        print('Non-JSON response:', resp.data.decode(errors='replace'))
    print('\n---\n')
