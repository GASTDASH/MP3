from supabase import create_client, Client

url: str = "https://yuomdsktqooaxwfhvhfn.supabase.co"
key: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inl1b21kc2t0cW9vYXh3Zmh2aGZuIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MDc3NTg2MjAsImV4cCI6MjAyMzMzNDYyMH0.xf2Ab-A-pC8QukG-EpU1mg7-2ybbV-mjDEVXwPhcaXM"
supabase: Client = create_client(url, key)

response = supabase.table('accounts').select("*").execute()
print(response)