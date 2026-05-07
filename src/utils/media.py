import httpx
import os
async def download_file(url, filename, save_dir='temp_media'):
    if not os.path.exists(save_dir): os.makedirs(save_dir)
    path = os.path.join(save_dir, filename)
    async with httpx.AsyncClient() as client:
        resp = await client.get(url, follow_redirects=True)
        if resp.status_code == 200:
            with open(path, 'wb') as f: f.write(resp.content)
            return path
    return ''