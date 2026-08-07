#!/usr/bin/env python3
"""Generate placeholder cards for all scene steps in 'The rich Abuja girl' storyboard.

Uses Pillow to render rich dark-emerald & gold luxury themed 16:9 visual tiles
with scene titles, step labels, and vignette effects.
"""

import random
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent
ACTS_DIR = {
    1: ROOT / "images" / "act1",
    2: ROOT / "images" / "act2",
    3: ROOT / "images" / "act3",
    4: ROOT / "images" / "act4",
    5: ROOT / "images" / "act5",
}

SCENE_ACT_MAP = {
    "S01": 1, "S02": 1, "S03": 1, "S04": 1, "S05": 1,
    "S06": 2, "S07": 2, "S08": 2, "S09": 2, "S10": 2,
    "S11": 3, "S12": 3, "S13": 3, "S14": 3, "S15": 3,
    "S16": 4, "S17": 4, "S18": 4, "S19": 4, "S20": 4,
    "S21": 5, "S22": 5, "S23": 5, "S24": 5, "S25": 5,
}

SCENE_TITLES = {
    "S01": "The Heiress of Maitama",
    "S02": "Broken Down on Shehu Shagari Way",
    "S03": "The First Encounter",
    "S04": "Coffee in Wuse II",
    "S05": "Chief Adenuga's Warning",
    "S06": "Sunset at Jabi Lake",
    "S07": "Tunde's Solar Workshop",
    "S08": "Bisi's Advice",
    "S09": "The Stolen Moment at Millennium Park",
    "S10": "The First Kiss",
    "S11": "The Gala Announcement",
    "S12": "Segun's Arrogance",
    "S13": "Tunde Gatecrashes",
    "S14": "Chief Adenuga's Confrontation",
    "S15": "The Ultimatum",
    "S16": "Segun's Sabotage",
    "S17": "Tiwa Stands Her Ground",
    "S18": "Rain at the National Mosque Vista",
    "S19": "The Green Energy Pitch",
    "S20": "Chief Adenuga Watches",
    "S21": "The Federal Contract Won",
    "S22": "Chief Adenuga's Blessing",
    "S23": "The Traditional Yoruba Igbeyawo",
    "S24": "The Church & White Wedding",
    "S25": "The Rich Abuja Girl's True Wealth",
}

STEP_DESCRIPTIONS = {
    "S01": ["maitama_mansion_wide", "tiwa_in_silk", "marble_staircase", "chief_adenuga_in_office", "bisi_visiting", "tiwa_at_balcony", "driver_ready", "suv_departure", "luxury_gates_open", "city_view"],
    "S02": ["rainy_expressway", "flat_tire_closeup", "driver_panicked", "pickup_truck_approaches", "tunde_steps_out", "tools_in_hand", "rain_pouring", "traffic_passing", "tiwa_watching", "tunde_smiles"],
    "S03": ["tunde_under_car", "tiwa_holding_umbrella", "engine_fixed", "grease_on_hands", "first_eye_contact", "tiwa_offers_cash", "tunde_declines", "coffee_proposal", "car_starts", "driving_to_wuse"],
    "S04": ["wuse_cafe_exterior", "espresso_tables", "tiwa_and_tunde_talking", "laughter_moment", "tunde_explains_solar", "tiwa_intrigued", "phone_numbers_exchanged", "leaving_cafe", "tunde_drops_tiwa", "adenuga_mansion_arrival"],
    "S05": ["chief_adenuga_at_gate", "cold_glare", "tunde_drives_off", "chief_confronts_tiwa", "family_status_speech", "tiwa_protests", "chief_demands_loyalty", "tiwa_in_bedroom", "looking_at_phone", "conflict_begins"],
    "S06": ["jabi_lake_boardwalk", "sunset_reflections", "tiwa_and_tunde_walking", "suya_vendor_nearby", "deep_conversation", "dreams_shared", "water_ripples", "holding_hands", "dusk_falling", "warm_embrace"],
    "S07": ["solar_workshop_wide", "circuit_boards", "tunde_soldering", "rural_grid_prototype", "tiwa_impressed", "sparks_flying", "tunde_passion", "blueprint_review", "tea_break", "shared_vision"],
    "S08": ["tiwa_fashion_studio", "bisi_arrives", "gossip_session", "bisi_teasing", "tiwa_blushing", "sketches_on_desk", "bisi_encouragement", "class_warning", "friendship_bond", "decision_made"],
    "S09": ["millennium_park_trees", "grassy_lawn", "secret_picnic", "tunde_promises", "tiwa_smiles", "birds_overhead", "afternoon_sun", "holding_palms", "comfort_in_love", "walking_together"],
    "S10": ["lake_at_night", "city_lights_far", "soft_breeze", "stepping_close", "first_kiss", "holding_tight", "spark_ignited", "moonlight_on_water", "whispered_words", "bound_together"],
    "S11": ["asokoro_ballroom", "glittering_chandelier", "high_society_guests", "chief_adenuga_on_stage", "segun_lawson_in_suit", "marriage_announcement", "tiwa_shocked", "applause", "segun_smirking", "tiwa_trapped"],
    "S12": ["segun_approaches_tiwa", "possessive_hand", "arrogant_words", "tiwa_pulls_away", "segun_chuckles", "bisi_glaring", "power_couple_claim", "champagne_toast", "tiwa_distressed", "looking_for_exit"],
    "S13": ["ballroom_doors_open", "tunde_in_dark_suit", "delivering_proposal", "eye_contact_across_room", "segun_notices", "chief_adenuga_frowns", "tension_rising", "tunde_unfazed", "tiwa_heart_racing", "confrontation_imminent"],
    "S14": ["private_study_doors", "chief_adenuga_confronts", "threat_to_buy_workshop", "tunde_stands_firm", "money_vs_honor", "chief_points_finger", "tunde_calm_resolve", "tiwa_listening_outside", "heated_words", "tunde_exits"],
    "S15": ["tiwa_confronts_father", "ultimatum_spoken", "chief_firm", "tiwa_tears", "segun_ring_brought", "refusal_to_submit", "stormy_night", "tiwa_locked_in", "phone_taken", "resolve_strengthened"],
    "S16": ["workshop_bank_notice", "locked_padlock", "tunde_outside", "segun_driving_by", "mocking_wave", "power_cut", "team_disheartened", "tunde_clenched_fists", "refusing_to_quit", "alternative_plan"],
    "S17": ["tiwa_confronts_segun", "glass_table_ring", "ring_thrown_down", "chief_adenuga_watching", "segun_humiliated", "tiwa_walks_out", "bisi_waiting_car", "escape_from_mansion", "freedom_chosen", "rain_starting"],
    "S18": ["national_mosque_vista", "cityline_in_rain", "tunde_in_thought", "tiwa_arrives", "umbrella_shared", "holding_hands_in_storm", "pitch_preparation", "bisi_media_campaign", "hope_rekindled", "united_front"],
    "S19": ["federal_ministry_hall", "board_members", "tunde_on_podium", "presentation_slides", "tiwa_in_audience", "bisi_filming", "tunde_eloquent", "solar_solution_demonstrated", "applause_building", "board_impressed"],
    "S20": ["back_of_auditorium", "chief_adenuga_seated", "watching_tunde", "respect_dawning", "segun_panicking", "board_deliberation", "chief_nods_slowly", "truth_recognized", "tiwa_sees_father", "shift_in_tide"],
    "S21": ["contract_signing", "tunde_awarded_tender", "standing_ovation", "segun_walks_out", "tiwa_runs_to_tunde", "joyful_hug", "cameras_flashing", "bisi_cheering", "chief_approaching", "new_beginning"],
    "S22": ["maitama_garden_sunlight", "chief_adenuga_invites_tunde", "handshake_offered", "father_apology", "blessing_given", "tiwa_happy_tears", "family_reconciliation", "wedding_plans", "aso_ebi_chosen", "unity_achieved"],
    "S23": ["yoruba_igbeyawo_grand", "blue_aso_oke_attire", "tunde_prostrating", "chief_blessing_head", "tiwa_gele_crown", "talking_drums", "dancing_guests", "bisi_dancing", "rings_exchanged", "tradition_honored"],
    "S24": ["abuja_cathedral_exterior", "stained_glass_interior", "tiwa_white_gown", "father_walks_tiwa", "tunde_at_altar", "vows_spoken", "holy_matrimony", "kiss_the_bride", "cheering_congregation", "car_with_ribbons"],
    "S25": ["jabi_lake_years_later", "sunshine_bright", "child_running", "tiwa_and_tunde_embracing", "looking_at_horizon", "peaceful_sunset", "true_wealth_found", "love_victorious", "final_frame", "fade_to_gold"],
}

def generate_scene_placeholders():
    print("Generating scene step placeholders for 'The rich Abuja girl'...")
    
    for scene_id, act_num in SCENE_ACT_MAP.items():
        act_dir = ACTS_DIR[act_num]
        steps = STEP_DESCRIPTIONS.get(scene_id, [f"step_{i}" for i in range(1, 11)])
        
        for i, step_desc in enumerate(steps, 1):
            filename = f"{scene_id}_Step{i:02d}_{step_desc}.jpg"
            filepath = act_dir / filename
            
            # Skip if real image already exists
            if filepath.exists():
                print(f"Skipping existing: {filename}")
                continue
                
            # Create a 16:9 dark emerald & gold Nigerian luxury theme card
            w, h = 960, 540
            img = Image.new('RGB', (w, h), (10, 30, 22))
            draw = ImageDraw.Draw(img)
            
            # Gradient fill (Emerald to deep navy)
            rng = random.Random(hash(f"{scene_id}_{i}"))
            for y in range(h):
                r = int(10 + (y / h) * 15)
                g = int(35 + (y / h) * 20)
                b = int(25 + (y / h) * 25)
                draw.line([(0, y), (w, y)], fill=(r, g, b))
                
            # Gold decorative frame border
            draw.rectangle([20, 20, w - 20, h - 20], outline=(212, 175, 55), width=2)
            draw.rectangle([24, 24, w - 24, h - 24], outline=(212, 175, 55), width=1)
            
            # Text rendering
            title = f"{scene_id} — Step {i:02d}"
            subtitle = SCENE_TITLES.get(scene_id, "")
            desc_text = step_desc.replace("_", " ").title()
            
            # Simple text overlay using default font
            draw.text((40, 40), f"ACT {act_num}", fill=(212, 175, 55))
            draw.text((40, 70), title, fill=(255, 255, 255))
            draw.text((40, 100), subtitle, fill=(180, 220, 195))
            draw.text((40, h - 60), f"Visual Concept: {desc_text}", fill=(212, 175, 55))
            
            img.save(filepath, format="JPEG", quality=85)
            print(f"Generated tile: {filename}")

if __name__ == "__main__":
    generate_scene_placeholders()
