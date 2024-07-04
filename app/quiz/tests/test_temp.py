import pytest


@pytest.mark.skip('testing test =\\')
async def test_aminio_url():
    client = Minio('localhost:9000', access_key='admin', secret_key='adminadmin', secure=False)
    bucket_name = 'main'
    object_name = '115 5 Lost Vikings.mp4'
    objs = []
    for i in range(100):
        objs.append(await client.presigned_get_object(bucket_name, object_name))

    a = 1

@pytest.mark.skip('testing test =\\')
def test_minio_url():
    client = Minio('localhost:9000', access_key='admin', secret_key='adminadmin', secure=False)
    bucket_name = 'main'
    object_name = '115 5 Lost Vikings.mp4'
    objs = []
    for i in range(10):
        objs.append(client.presigned_get_object(bucket_name, object_name))

    a = 1

@pytest.mark.skip('testing test =\\')
def test_put_file():
    client = Minio('localhost:9000', access_key='admin', secret_key='adminadmin', secure=False)
    bucket = 'testput'

    # with open('.sources/wensday.mp4', 'rb') as file_data:
        # client.put_object(bucket, 'file1.mp4', file_data, length=file_data.seek(0, 2))

    t1 = time.time()
    for i in range(1):
        client.fput_object(bucket, f'wensday.mp4', '.sources/wensday.mp4')
    print(time.time() - t1)

@pytest.mark.skip('testing test =\\')
async def async_upload_file(client, bucket, file_name, file_path):
    await client.fput_object(bucket, file_name, file_path)

@pytest.mark.skip('testing test =\\')
async def test_async_put_file():
    client = Minio('localhost:9000', access_key='admin', secret_key='adminadmin', secure=False)
    bucket = 'testput'
    tasks = []
    for i in range(2):
        tasks.append(async_upload_file(client, bucket, f'file-{str(i)}.mp4', '.sources/video.mov'))
    await asyncio.gather(*tasks)

@pytest.mark.skip('testing test =\\')
async def test_async_put_file2():
    client = Minio('localhost:9000', access_key='admin', secret_key='adminadmin', secure=False)
    bucket = 'testput'
    for i in range(2):
        await client.fput_object(bucket, f'file-{str(i)}.mp4', '.sources/video.mov')