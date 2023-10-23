from power_systems_data_api_demonstrator.src.api.seed import seed_generation


def test_seed(session):
    seed_generation(session)
