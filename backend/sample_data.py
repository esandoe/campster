import random
from database import SupplyTarget, Trip, TripParticipant, ParticipantItem, User

ids = list(range(1, 5))

sample_users = [
    User(id=ids.pop(random.randint(0, len(ids) - 1)), name="Rin Shima"),
    User(id=ids.pop(random.randint(0, len(ids) - 1)), name="Nadeshiko Kagamihara"),
    User(id=ids.pop(random.randint(0, len(ids) - 1)), name="Aoi Inuyama"),
    User(id=ids.pop(random.randint(0, len(ids) - 1)), name="Chiaki Oogaki"),
]

tent_target = SupplyTarget(trip_id=1, name="Soveplass i telt", target_quantity=3)
gas_stove_target = SupplyTarget(trip_id=1, name="Gassbrenner", target_quantity=1)
gas_canister_target = SupplyTarget(
    trip_id=1, name="Liten Gassbeholder", target_quantity=2
)
pot_target = SupplyTarget(trip_id=1, name="Kjele", target_quantity=2)
pan_target = SupplyTarget(trip_id=1, name="Stekepanne", target_quantity=1)
bread_target = SupplyTarget(trip_id=1, name="Brød", target_quantity=1)
butter_target = SupplyTarget(trip_id=1, name="Smør", target_quantity=1)
cheese_target = SupplyTarget(trip_id=1, name="Ost", target_quantity=1)
ketchup_target = SupplyTarget(trip_id=1, name="Ketchup", target_quantity=1)

sample_participant_items = [
    ("12 personers glamping lavvo", tent_target, 12),
    ("2 personers telt", tent_target, 2),
    ("Zenbivy sovesystem", None, 1),
    ("Gryte Liten", pot_target, 1),
    ("Gryte Stor", pot_target, 1),
    ("Gassbrenner", gas_stove_target, 1),
    ("Liten Gassbeholder", gas_canister_target, 1),
    ("Stekepanne", pan_target, 1),
    ("Brød", bread_target, 1),
    ("Smør", butter_target, 1),
    ("Ost", cheese_target, 1),
    ("Ketchup", ketchup_target, 1),
    ("Sovepose", None, 1),
    ("Turmat", None, 1),
    ("Fiskestang", None, 1),
    ("Fiskekrok", None, 1),
    ("Fiskeagn", None, 1),
]

sample_trips = [
    Trip(
        name="Glamping i Lofoten",
        participants=[
            TripParticipant(
                user_id=user.id,
                trip_id=1,
                items=[
                    ParticipantItem(supply_target=target, name=name, quantity=quantity)
                    for (name, target, quantity) in random.sample(
                        sample_participant_items, 8
                    )
                ],
            )
            for user in random.sample(sample_users, 3)
        ],
    )
]
