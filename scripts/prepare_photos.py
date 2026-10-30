"""Curate downloaded web references; preserve originals and source attribution."""
import json, shutil
from pathlib import Path
rows = {
1: [('honda-pcx-160-warna-putih-cbs', [2], 'https://beritamotor.net/warna-honda-pcx-160-2023/'), ('honda-pcx-160-product-motorcycle', [2], 'https://www.bikedekho.com/honda/pcx150'), ('honda-pcx-160-product-motorcycle',[3,4],'https://www.zigwheels.ph/new-motorcycles/honda/pcx160')],
2: [('yamaha-nmax-neo-product-warna-white-red',[1,2],'https://goozir.com/motor-yamaha-nmax-neo/'),('site-oto-com-yamaha-nmax-neo-gambar',[3,4],'https://www.yamahabrm.co.id/product/Nmax-Neo')],
3: [('honda-vario-160-cbs-black-motor',[1],'https://www.bikes4sale.in/details/honda/vario/vario-160/'),('honda-vario-160-motorcycle',[1,3],'https://www.oto.com/en/motor-baru/honda/vario-160/gambar'),('site-oto-com-honda-vario-160-gambar-fron',[1],'https://www.oto.com/motor-baru/honda/vario-160')],
4: [('site-oto-com-alva-cervo-gambar',[2],'https://www.liputan6.com/otomotif/read/5300465/motor-listrik-alva-cervo-resmi-hadir-di-indonesia-harga-mulai-rp-3775-juta'),('alva-cervo-motor-listrik',[3],'https://www.jawapos.com/otomotif/012902763/mengenal-cervo-motor-listrik-alva-berikan-fitur-kekinian'),('alva-cervo-motor-listrik',[4],'https://www.idntimes.com/automotive/motorbike/motor-listrik-alva-cervo-harga-spesifikasi-fitur-00-kkx41-14qh8m'),('site-oto-com-alva-cervo-gambar',[3],'https://www.oto.com/berita-motor/skema-kredit-alva-cervo-dp-mulai-rp6-juta-dan-angsuran-rp500-ribuan')],
5: [('site-oto-com-kawasaki-ninja-250-gambar-f',[2],'https://oto.com/berita-motor/kilas-balik-perjalanan-kawasaki-ninja-250-di-indonesia'),('site-oto-com-kawasaki-ninja-250-gambar-f',[3],'https://www.oto.com/motor-baru/kawasaki/ninja-250/video'),('site-oto-com-kawasaki-ninja-250-gambar-f',[4],'https://www.oto.com/bandingkan-motor/kawasaki-ninja-250-and-kawasaki-z250'),('kawasaki-ninja-250-2023-detail-motorcycl',[2],'https://tmmotoworld.com/product/2023-kawasaki-ninja-250')],
6: [('suzuki-satria-f150-motorcycle',[4],'https://www.oto.com/en/motor-baru/suzuki/satria-f150/gambar'),('suzuki-satria-f150-motorcycle',[2],'https://paultan.org/2016/08/17/giias-2016-suzuki-satria-f150-one-we-will-not-have'),('suzuki-satria-f150-motorcycle',[3],'https://www.zigwheels.vn/en/new-motorcycles/suzuki/satria-f150/specifications'),('suzuki-satria-f150-headlight-speedometer',[2],'https://www.oto.com/berita-motor/suzuki-satria-f150-my-2026-kepergok-tes-jalan-mau-meluncur-di-indonesia')],
7: [('site-oto-com-vespa-primavera-150-gambar',[1],'https://uscoots.com/products/vespa-primavera-150'),('site-oto-com-vespa-primavera-150-gambar',[2],'https://motorcycles.autotrader.com/motorcycles-for-sale/vespa-primavera_150-for-sale'),('site-oto-com-vespa-primavera-150-gambar',[4],'https://crmotos.com/modelo/vespa-primavera-150'),('vespa-primavera-scooter',[1],'https://www.zigwheels.ph/new-motorcycles/vespa/primavera')],
8: [('polytron-fox-r-motor-listrik',[3,4],'https://www.sinarmaju.co.id/motor-listrik-polytron-fox-r'),('polytron-fox-r-motor-listrik',[1],'https://astraotoshop.com/article/spesifikasi-motor-listrik-polytron-fox-r'),('polytron-fox-r-motor-listrik',[2],'https://kumparan.com/info-produk/spesifikasi-motor-listrik-polytron-fox-r-beserta-harganya-22suj16Z94y')],
9: [('tvs-ronin-motorcycle',[1],'https://www.tvsmotor.com/media/blog/tvs-ronin-reasons-to-ride-unscripted'),('tvs-ronin-motorcycle',[2],'https://www.bikewale.com/tvs-bikes/ronin/'),('tvs-ronin-motorcycle',[3],'https://www.oto.com/en/motor-baru/tvs/ronin/gambar'),('tvs-ronin-motorcycle',[4],'https://autos.maxabout.com/bikes/tvs/ronin')],
10: [('royal-enfield-hunter-350-motorcycle',[3],'https://motohunt.com/motorcycles-for-sale/Royal-Enfield-Hunter-350'),('royal-enfield-hunter-350-motorcycle',[1],'https://www.autox.com/new-bikes/royal-enfield/hunter-350/photos/'),('royal-enfield-hunter-350-motorcycle',[2],'https://en.wikipedia.org/wiki/Royal_Enfield_Hunter_350'),('royal-enfield-hunter-350-motorcycle',[4],'https://www.oto.com/en/motor-baru/royal-enfield/hunter-350/gambar')],
11: [('united-t1800-motor-product-white',[2],'https://www.oto.com/motor-baru/united/t1800'),('united-t1800-motor-listrik',[4],'https://kumparan.com/kumparanoto/foto-united-e-motor-t1800-motor-listrik-saingan-gesits-seharga-rp-27-juta-1ulbUmzDIzv'),('united-t1800-motor-listrik',[2],'https://otomotif.antaranews.com/berita/1892488/spesifikasi-dan-target-penjualan-motor-listrik-united-t1800'),('united-t1800-motor-product-white',[1],'https://www.dinomarket.com/TD/30178732/United-Motor-Listrik-T1800-White/')],
12: [('yadea-g6-motor-listrik',[1],'https://otorider.com/motor-listrik/2023/galeri-melihat-lebih-detail-motor-listrik-yadea-g6-galcgdicag6'),('yadea-g6-motor-listrik',[2,3],'https://otomotif.kompas.com/read/2023/02/28/154100415/tes-singkat-motor-listrik-yadea-g6-seharga-rp-29-jutaan'),('yadea-g6-detail-lampu-motor',[2],'https://gadget.viva.co.id/ecommerce/8580-yadea-g6-motor-listrik-dengan-subsidi-7-juta-dari-pemerintah-cek-harganya-sekarang')]
}
out=Path('public/photos');out.mkdir(exist_ok=True)
manifest={}
for bike, groups in rows.items():
    manifest[bike]=[]
    for prefix, indices, source in groups:
        for n in indices:
            original=next(Path('image-search').glob(f'{prefix}-{n}.*'))
            name=f'{bike}-{len(manifest[bike])+1}{original.suffix}'
            shutil.copyfile(original,out/name)
            manifest[bike].append({'src':f'/photos/{name}','source':source,'label':f'Foto referensi {len(manifest[bike])+1}','rights':'Hak cipta pemilik sumber; izin komersial belum diverifikasi.'})
    assert len(manifest[bike])==4
Path('src/photos.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False))
print('Prepared',sum(map(len,manifest.values())),'photos')
