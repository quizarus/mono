

async def test_get_packs(async_client, pack):
    response = await async_client.get('quiz/packs')
    assert response.status_code == 200
    assert response.json()


async def test_get_pack(async_client, pack):
    response = await async_client.get(f'quiz/packs/{pack.id}')
    assert response.status_code == 200
    assert response.json()


async def test_get_questions(async_client, question):
    response = await async_client.get('quiz/questions')
    assert response.status_code == 200
    assert response.json()


async def test_get_answers(async_client, answer):
    response = await async_client.get('quiz/answers')
    assert response.status_code == 200
    assert response.json()