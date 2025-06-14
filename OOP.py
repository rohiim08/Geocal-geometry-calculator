# ============== Main =========================
from abc import ABC, abstractmethod
import math

# ============================ Class Abstrak ============================

class BangunDatar(ABC):              
    @abstractmethod         
    def luas(self):                  
        pass

    @abstractmethod
    def keliling(self):
        pass

class BangunRuang(ABC):              
    @abstractmethod
    def luas_permukaan(self):        
        pass

    @abstractmethod
    def volume(self):
        pass

# ============================ Bangun Datar ============================

# 1. Persegi - (Aldhan)
class Persegi(BangunDatar):
    def __init__(self, sisi):
        self.sisi = sisi

    def luas(self):
        return self.sisi * self.sisi

    def keliling(self):
        return 4 * self.sisi

# 2. Persegi - Panjang (Aldhan)
class PersegiPanjang(BangunDatar):
    def __init__(self, panjang, lebar):
        self.panjang = panjang
        self.lebar = lebar

    def luas(self):
        return self.panjang * self.lebar

    def keliling(self):
        return 2 * (self.panjang + self.lebar)

# 3. Segitiga - (Rohim)
class Segitiga(BangunDatar):
    def __init__(self, alas, tinggi, sisi):
        self.alas = alas
        self.tinggi = tinggi
        self.sisi = sisi

    def luas(self):
        return (self.alas * self.tinggi) / 2

    def keliling(self):
        return self.alas + self.tinggi + self.sisi

# 4. Lingkaran - (Rohim)
class Lingkaran(BangunDatar):
    def __init__(self, jari_jari):
        self.jari_jari = jari_jari

    def luas(self):
        return math.pi * (self.jari_jari ** 2)

    def keliling(self):
        return 2 * math.pi * self.jari_jari

# 5. Jajargenjang - (Rizki)
class JajarGenjang(BangunDatar):
    def __init__(self, alas, sisi_miring, tinggi):
        self.alas = alas
        self.sisi_miring = sisi_miring
        self.tinggi = tinggi

    def luas(self):
        return (self.alas * self.tinggi)

    def keliling(self):
        return 2 * (self.alas + self.sisi_miring)

# 6. Trapesium - (Rizki)
class Trapesium(BangunDatar):
    def __init__(self, sisi_atas, sisi_bawah, sisi_kiri, sisi_kanan, tinggi):
        self.sisi_atas = sisi_atas
        self.sisi_bawah = sisi_bawah
        self.sisi_kiri = sisi_kiri
        self.sisi_kanan = sisi_kanan
        self.tinggi = tinggi

    def luas(self):
        return ((self.sisi_atas + self.sisi_bawah) * self.tinggi) / 2

    def keliling(self):
        return (self.sisi_atas + self.sisi_bawah + self.sisi_kiri + self.sisi_kanan)

# 7. Belah Ketupat - (Zakka)
class BelahKetupat(BangunDatar):
    def __init__(self, diagonal1, diagonal2, sisi):
        self.diagonal1 = diagonal1
        self.diagonal2 = diagonal2
        self.sisi = sisi

    def luas(self):
        return (self.diagonal1 * self.diagonal2) / 2

    def keliling(self):
        return 4 * self.sisi

# 8. Layang-Layang - (Zakka)
class LayangLayang(BangunDatar):
    def __init__(self, diagonal1, diagonal2, sisi1, sisi2):
        self.diagonal1 = diagonal1
        self.diagonal2 = diagonal2
        self.sisi1 = sisi1
        self.sisi2 = sisi2

    def luas(self):
        return (self.diagonal1 * self.diagonal2) / 2

    def keliling(self):
        return 2 * (self.sisi1 + self.sisi2)

# ============================ Bangun Ruang ============================

# 1. Kubus - (Aldhan)
class Kubus(BangunRuang):
    def __init__(self, sisi):
        self.sisi = sisi

    def volume(self):
        return self.sisi ** 3

    def luas_permukaan(self):
        return 6 * (self.sisi ** 2)

# 2. Balok - (Aldhan)
class Balok(BangunRuang):
    def __init__(self, panjang, lebar, tinggi):
        self.panjang = panjang
        self.lebar = lebar
        self.tinggi = tinggi

    def volume(self):
        return self.panjang * self.lebar * self.tinggi

    def luas_permukaan(self):
        return 2 * (self.panjang * self.lebar + self.panjang * self.tinggi + self.lebar * self.tinggi)
# 3. Limas Segiempat - (Rohim)
class LimasSegiempat(BangunRuang):
    def __init__(self, sisi_alas, tinggi):
        self.sisi_alas = sisi_alas
        self.tinggi = tinggi

    def volume(self):
        return (self.sisi_alas ** 2) * self.tinggi / 3

    def luas_permukaan(self):
        luas_alas = self.sisi_alas ** 2
        luas_sisi = 2 * self.sisi_alas * self.tinggi
        return luas_alas + luas_sisi

# 4. Limas Segitiga - (Rohim)
class LimasSegitiga(BangunRuang):
    def __init__(self, alas, tinggi_alas, tinggi):
        self.alas = alas
        self.tinggi_alas = tinggi_alas
        self.tinggi = tinggi

    def volume(self):
        return (self.alas * self.tinggi_alas * self.tinggi) / 3

    def luas_permukaan(self):
        luas_alas = (self.alas * self.tinggi_alas) / 2
        luas_sisi = (self.alas * self.tinggi) / 2
        return luas_alas + (3 * luas_sisi)

# 5. Prisma Segitiga - (Rizki)
class Prisma(BangunRuang):
    def __init__(self, alas, tinggi_alas, tinggi_prisma, jumlah_sisi_alas):
        self.alas = alas
        self.tinggi_alas = tinggi_alas
        self.tinggi_prisma = tinggi_prisma
        self.jumlah_sisi_alas = jumlah_sisi_alas
    
    def volume(self):
        luas_alas = 0.5 * self.alas * self.tinggi_alas
        return luas_alas * self.tinggi_prisma

    def luas_permukaan(self):
        keliling_alas = self.jumlah_sisi_alas * self.alas
        luas_alas = 0.5 * self.alas * self.tinggi_alas
        return 2 * luas_alas + keliling_alas * self.tinggi_prisma
    
# 6. Tabung - (Rizki)
class Tabung(BangunRuang):
    def __init__(self, jari_jari, tinggi):
        self.jari_jari = jari_jari
        self.tinggi = tinggi
    
    def volume(self):
        return 3.14 * (self.jari_jari ** 2) * self.tinggi

    def luas_permukaan(self):
        return 2 * 3.14 * self.jari_jari * (self.jari_jari + self.tinggi)
    
# 7. Kerucut - (Zakka)
class Kerucut(BangunRuang):
    def __init__(self, jari_jari, tinggi):
        self.jari_jari = jari_jari
        self.tinggi = tinggi
        self.garis_pelukis = math.sqrt((self.jari_jari * self.jari_jari) + (self.tinggi * self.tinggi))

    def volume(self):
        return (1/3) * math.pi * (self.jari_jari * self.jari_jari) * self.tinggi

    def luas_permukaan(self):
        return math.pi * self.jari_jari * (self. jari_jari + self.garis_pelukis)

# 8. Bola - (Zakka)
class Bola(BangunRuang):
    def __init__(self, jari_jari):
        self.jari_jari = jari_jari

    def volume(self):
        return (4/3) * math.pi * (self.jari_jari * self.jari_jari * self.jari_jari)

    def luas_permukaan(self):
        return 4 * math.pi * (self.jari_jari * self.jari_jari)