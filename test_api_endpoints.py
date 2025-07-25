import requests
import json
from datetime import datetime, timedelta

BASE_URL = "http://localhost:8000/api/v1"
EMAIL = "admin@eshow.com"
PASSWORD = "admin123"

def print_response(title, resp):
    print(f"\n=== {title} ===")
    print(f"Status: {resp.status_code}")
    try:
        print(json.dumps(resp.json(), indent=2, ensure_ascii=False))
    except Exception:
        print(resp.text)

def main():
    print("# TESTE COMPLETO DE TODOS OS ENDPOINTS")
    print("=" * 50)
    
    # 1. AUTENTICAÇÃO
    print("\n# 1. AUTENTICAÇÃO")
    login_resp = requests.post(f"{BASE_URL}/auth/login", json={"email": EMAIL, "password": PASSWORD})
    print_response("Login", login_resp)
    assert login_resp.status_code == 200, "Falha no login"
    token = login_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    # 2. USUÁRIOS
    print("\n# 2. USUÁRIOS")
    # GET /me
    resp = requests.get(f"{BASE_URL}/users/me", headers=headers)
    print_response("Get Current User", resp)
    
    # GET /users
    resp = requests.get(f"{BASE_URL}/users/", headers=headers)
    print_response("List Users", resp)
    
    # GET /users/{user_id}
    resp = requests.get(f"{BASE_URL}/users/5", headers=headers)
    print_response("Get User by ID", resp)
    
    # 3. PROFILES
    print("\n# 3. PROFILES")
    # GET /profiles
    resp = requests.get(f"{BASE_URL}/profiles/", headers=headers)
    print_response("List Profiles", resp)
    
    # GET /profiles/{profile_id}
    resp = requests.get(f"{BASE_URL}/profiles/1", headers=headers)
    print_response("Get Profile by ID", resp)
    
    # GET /profiles/role/{role_id}
    resp = requests.get(f"{BASE_URL}/profiles/role/1", headers=headers)
    print_response("Get Profiles by Role", resp)
    
    # 4. ROLES
    print("\n# 4. ROLES")
    # GET /roles
    resp = requests.get(f"{BASE_URL}/roles/", headers=headers)
    print_response("List Roles", resp)
    
    # GET /roles/{role_id}
    resp = requests.get(f"{BASE_URL}/roles/1", headers=headers)
    print_response("Get Role by ID", resp)
    
    # 5. ARTIST TYPES
    print("\n# 5. ARTIST TYPES")
    # GET /artist-types
    resp = requests.get(f"{BASE_URL}/artist-types/", headers=headers)
    print_response("List Artist Types", resp)
    
    # GET /artist-types/{artist_type_id}
    resp = requests.get(f"{BASE_URL}/artist-types/1", headers=headers)
    print_response("Get Artist Type by ID", resp)
    
    # 6. MUSICAL STYLES
    print("\n# 6. MUSICAL STYLES")
    # GET /musical-styles
    resp = requests.get(f"{BASE_URL}/musical-styles/", headers=headers)
    print_response("List Musical Styles", resp)
    
    # GET /musical-styles/{style_id}
    resp = requests.get(f"{BASE_URL}/musical-styles/1", headers=headers)
    print_response("Get Musical Style by ID", resp)
    
    # 7. EVENT TYPES
    print("\n# 7. EVENT TYPES")
    # GET /event-types
    resp = requests.get(f"{BASE_URL}/event-types/", headers=headers)
    print_response("List Event Types", resp)
    
    # GET /event-types/{event_type_id}
    resp = requests.get(f"{BASE_URL}/event-types/1", headers=headers)
    print_response("Get Event Type by ID", resp)
    
    # 8. FESTIVAL TYPES
    print("\n# 8. FESTIVAL TYPES")
    # GET /festival-types
    resp = requests.get(f"{BASE_URL}/festival-types/", headers=headers)
    print_response("List Festival Types", resp)
    
    # GET /festival-types/{festival_type_id}
    resp = requests.get(f"{BASE_URL}/festival-types/1", headers=headers)
    print_response("Get Festival Type by ID", resp)
    
    # 9. SPACE TYPES
    print("\n# 9. SPACE TYPES")
    # GET /space-types
    resp = requests.get(f"{BASE_URL}/space-types/", headers=headers)
    print_response("List Space Types", resp)
    
    # GET /space-types/{space_type_id}
    resp = requests.get(f"{BASE_URL}/space-types/1", headers=headers)
    print_response("Get Space Type by ID", resp)
    
    # 10. SPACES
    print("\n# 10. SPACES")
    # GET /spaces
    resp = requests.get(f"{BASE_URL}/spaces/", headers=headers)
    print_response("List Spaces", resp)
    
    # GET /spaces/{space_id}
    resp = requests.get(f"{BASE_URL}/spaces/1", headers=headers)
    print_response("Get Space by ID", resp)
    
    # 11. ARTISTS
    print("\n# 11. ARTISTS")
    # GET /artists
    resp = requests.get(f"{BASE_URL}/artists/", headers=headers)
    print_response("List Artists", resp)
    
    # GET /artists/{artist_id}
    resp = requests.get(f"{BASE_URL}/artists/1", headers=headers)
    print_response("Get Artist by ID", resp)
    
    # GET /artists/profile/{profile_id}
    resp = requests.get(f"{BASE_URL}/artists/profile/1", headers=headers)
    print_response("Get Artists by Profile", resp)
    
    # GET /artists/type/{artist_type_id}
    resp = requests.get(f"{BASE_URL}/artists/type/1", headers=headers)
    print_response("Get Artists by Type", resp)
    
    # 12. SPACE EVENT TYPES
    print("\n# 12. SPACE EVENT TYPES")
    # GET /space-event-types
    resp = requests.get(f"{BASE_URL}/space-event-types/", headers=headers)
    print_response("List Space Event Types", resp)
    
    # GET /space-event-types/{space_event_type_id}
    resp = requests.get(f"{BASE_URL}/space-event-types/1", headers=headers)
    print_response("Get Space Event Type by ID", resp)
    
    # GET /space-event-types/space/{space_id}
    resp = requests.get(f"{BASE_URL}/space-event-types/space/1", headers=headers)
    print_response("Get Space Event Types by Space", resp)
    
    # GET /space-event-types/event-type/{event_type_id}
    resp = requests.get(f"{BASE_URL}/space-event-types/event-type/1", headers=headers)
    print_response("Get Space Event Types by Event Type", resp)
    
    # GET /space-event-types/space/{space_id}/event-type/{event_type_id}
    resp = requests.get(f"{BASE_URL}/space-event-types/space/1/event-type/1", headers=headers)
    print_response("Get Space Event Types by Space and Event Type", resp)
    
    # 13. SPACE FESTIVAL TYPES
    print("\n# 13. SPACE FESTIVAL TYPES")
    # GET /space-festival-types
    resp = requests.get(f"{BASE_URL}/space-festival-types/", headers=headers)
    print_response("List Space Festival Types", resp)
    
    # GET /space-festival-types/{space_festival_type_id}
    resp = requests.get(f"{BASE_URL}/space-festival-types/1", headers=headers)
    print_response("Get Space Festival Type by ID", resp)
    
    # GET /space-festival-types/space/{space_id}
    resp = requests.get(f"{BASE_URL}/space-festival-types/space/1", headers=headers)
    print_response("Get Space Festival Types by Space", resp)
    
    # GET /space-festival-types/festival-type/{festival_type_id}
    resp = requests.get(f"{BASE_URL}/space-festival-types/festival-type/1", headers=headers)
    print_response("Get Space Festival Types by Festival Type", resp)
    
    # GET /space-festival-types/space/{space_id}/festival-type/{festival_type_id}
    resp = requests.get(f"{BASE_URL}/space-festival-types/space/1/festival-type/1", headers=headers)
    print_response("Get Space Festival Types by Space and Festival Type", resp)
    
    # 14. BOOKINGS
    print("\n# 14. BOOKINGS")
    # GET /bookings
    resp = requests.get(f"{BASE_URL}/bookings/", headers=headers)
    print_response("List Bookings", resp)
    
    # GET /bookings/{booking_id}
    resp = requests.get(f"{BASE_URL}/bookings/1", headers=headers)
    print_response("Get Booking by ID", resp)
    
    # GET /bookings/profile/{profile_id}
    resp = requests.get(f"{BASE_URL}/bookings/profile/1", headers=headers)
    print_response("Get Bookings by Profile", resp)
    
    # GET /bookings/space/{space_id}
    resp = requests.get(f"{BASE_URL}/bookings/space/1", headers=headers)
    print_response("Get Bookings by Space", resp)
    
    # GET /bookings/artist/{artist_id}
    resp = requests.get(f"{BASE_URL}/bookings/artist/1", headers=headers)
    print_response("Get Bookings by Artist", resp)
    
    # GET /bookings/space-event-type/{space_event_type_id}
    resp = requests.get(f"{BASE_URL}/bookings/space-event-type/1", headers=headers)
    print_response("Get Bookings by Space Event Type", resp)
    
    # GET /bookings/space-festival-type/{space_festival_type_id}
    resp = requests.get(f"{BASE_URL}/bookings/space-festival-type/1", headers=headers)
    print_response("Get Bookings by Space Festival Type", resp)
    
    # GET /bookings/date-range
    start_date = datetime.now().strftime("%Y-%m-%d")
    end_date = (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")
    resp = requests.get(f"{BASE_URL}/bookings/date-range?data_inicio={start_date}&data_fim={end_date}", headers=headers)
    print_response("Get Bookings by Date Range", resp)
    
    # 15. REVIEWS
    print("\n# 15. REVIEWS")
    # GET /reviews
    resp = requests.get(f"{BASE_URL}/reviews/", headers=headers)
    print_response("List Reviews", resp)
    
    # GET /reviews/{review_id}
    resp = requests.get(f"{BASE_URL}/reviews/2", headers=headers)
    print_response("Get Review by ID", resp)
    
    # GET /reviews/profile/{profile_id}
    resp = requests.get(f"{BASE_URL}/reviews/profile/1", headers=headers)
    print_response("Get Reviews by Profile", resp)
    
    # GET /reviews/profile/{profile_id}/average
    resp = requests.get(f"{BASE_URL}/reviews/profile/1/average", headers=headers)
    print_response("Get Profile Average Rating", resp)
    
    # GET /reviews/space-event-type/{space_event_type_id}
    resp = requests.get(f"{BASE_URL}/reviews/space-event-type/1", headers=headers)
    print_response("Get Reviews by Space Event Type", resp)
    
    # GET /reviews/space-festival-type/{space_festival_type_id}
    resp = requests.get(f"{BASE_URL}/reviews/space-festival-type/1", headers=headers)
    print_response("Get Reviews by Space Festival Type", resp)
    
    # GET /reviews/rating/{nota}
    resp = requests.get(f"{BASE_URL}/reviews/rating/5", headers=headers)
    print_response("Get Reviews by Rating", resp)
    
    # GET /reviews/date-range
    resp = requests.get(f"{BASE_URL}/reviews/date-range/?data_inicio={start_date}&data_fim={end_date}", headers=headers)
    print_response("Get Reviews by Date Range", resp)
    
    # 16. INTERESTS
    print("\n# 16. INTERESTS")
    # GET /interests
    resp = requests.get(f"{BASE_URL}/interests/", headers=headers)
    print_response("List Interests", resp)
    
    # GET /interests/{interest_id}
    resp = requests.get(f"{BASE_URL}/interests/1", headers=headers)
    print_response("Get Interest by ID", resp)
    
    # GET /interests/profile/interessado/{profile_id}
    resp = requests.get(f"{BASE_URL}/interests/profile/interessado/1", headers=headers)
    print_response("Get Interests by Profile Interessado", resp)
    
    # GET /interests/profile/interesse/{profile_id}
    resp = requests.get(f"{BASE_URL}/interests/profile/interesse/1", headers=headers)
    print_response("Get Interests by Profile Interesse", resp)
    
    # GET /interests/space-event-type/{space_event_type_id}
    resp = requests.get(f"{BASE_URL}/interests/space-event-type/1", headers=headers)
    print_response("Get Interests by Space Event Type", resp)
    
    # GET /interests/space-festival-type/{space_festival_type_id}
    resp = requests.get(f"{BASE_URL}/interests/space-festival-type/1", headers=headers)
    print_response("Get Interests by Space Festival Type", resp)
    
    # 17. FINANCIALS
    print("\n# 17. FINANCIALS")
    # GET /financials
    resp = requests.get(f"{BASE_URL}/financials/", headers=headers)
    print_response("List Financials", resp)
    
    # GET /financials/{financial_id}
    resp = requests.get(f"{BASE_URL}/financials/2", headers=headers)
    print_response("Get Financial by ID", resp)
    
    # 18. LOCATION SEARCH
    print("\n# 18. LOCATION SEARCH")
    # GET /location-search/spaces-for-artist
    resp = requests.get(f"{BASE_URL}/location-search/spaces-for-artist?cep=01310-100&raio_km=50&profile_id=3", headers=headers)
    print_response("Search Spaces for Artist", resp)
    
    # GET /location-search/artists-for-space
    resp = requests.get(f"{BASE_URL}/location-search/artists-for-space?cep=01310-100&raio_km=50&profile_id=2", headers=headers)
    print_response("Search Artists for Space", resp)
    
    # POST /location-search/spaces-for-artist
    search_payload = {
        "cep": "01310-100",
        "raio_km": 50,
        "return_ids_only": False,
        "profile_id": 3
    }
    resp = requests.post(f"{BASE_URL}/location-search/spaces-for-artist", headers=headers, json=search_payload)
    print_response("Search Spaces for Artist (POST)", resp)
    
    # POST /location-search/artists-for-space
    search_payload_space = {
        "cep": "01310-100",
        "raio_km": 50,
        "return_ids_only": False,
        "profile_id": 2
    }
    resp = requests.post(f"{BASE_URL}/location-search/artists-for-space", headers=headers, json=search_payload_space)
    print_response("Search Artists for Space (POST)", resp)
    
    # 19. ARTIST MUSICAL STYLES
    print("\n# 19. ARTIST MUSICAL STYLES")
    # GET /artist-musical-styles/artist/{artist_id}
    resp = requests.get(f"{BASE_URL}/artist-musical-styles/artist/1", headers=headers)
    print_response("Get Artist Musical Styles by Artist", resp)
    
    # GET /artist-musical-styles/musical-style/{musical_style_id}
    resp = requests.get(f"{BASE_URL}/artist-musical-styles/musical-style/1", headers=headers)
    print_response("Get Artist Musical Styles by Musical Style", resp)
    
    # GET /artist-musical-styles/{artist_id}/{musical_style_id}
    resp = requests.get(f"{BASE_URL}/artist-musical-styles/1/1", headers=headers)
    print_response("Get Artist Musical Style by Artist and Musical Style", resp)
    
    print("\n" + "=" * 50)
    print("TESTE COMPLETO FINALIZADO!")
    print("=" * 50)

if __name__ == "__main__":
    main() 