import asyncio
from telethon.sync import TelegramClient
from telethon.errors.rpcerrorlist import FloodWaitError

# --- KONFIGURASI ---
# Harap isi 2 baris yang ditandai di bawah ini
# -----------------------------------------------
API_ID = 12234  # (Dari screenshot Anda)
API_HASH = " " # <-- ISI INI (dari my.telegram.org)
PHONE_NUMBER = "-6200000000" # <-- ISI INI (cth: '+628529922992')
TARGET_GROUP_ID = -10011111111  # (ID Grup yang Anda berikan)
# -----------------------------------------------

async def main():
    # Menggunakan nama file sesi agar tidak perlu login berulang kali
    async with TelegramClient(PHONE_NUMBER, API_ID, API_HASH) as client:
        print("Klien berhasil terhubung...")

        try:
            # Menguji apakah kita bisa mendapatkan info tentang grup
            entity = await client.get_entity(TARGET_GROUP_ID)
            print(f"Berhasil terhubung ke grup: '{entity.title}'. Memulai penghapusan pesan...")

        except ValueError:
            print("Error: TARGET_GROUP_ID sepertinya tidak valid. Pastikan itu adalah angka.")
            return
        except Exception as e:
            print(f"Error saat mencoba mengakses grup: {e}")
            print("Pastikan Anda adalah anggota grup tersebut.")
            return

        # Iterasi dan hapus pesan
        count = 0
        try:
            # --- OPSI PENGHAPUSAN ---

            # 1. UNTUK MENGHAPUS PESAN ANDA SENDIRI:
            # async for message in client.iter_messages(TARGET_GROUP_ID, from_user='me'):
            
            # 2. UNTUK MENGHAPUS SEMUA PESAN (PERLU HAK ADMIN):
            # (Ini aktif secara default)
            async for message in client.iter_messages(TARGET_GROUP_ID):
                
                print(f"Menghapus pesan ID: {message.id}...")
                await message.delete()
                count += 1
                
                # Jeda singkat agar tidak kena 'FloodWaitError' dari Telegram
                await asyncio.sleep(0.5) 

        except FloodWaitError as e:
            print(f"Terkena Flood Wait. Telegram meminta untuk menunggu {e.seconds} detik.")
            print(f"Total {count} pesan telah dihapus sebelum berhenti.")
        except Exception as e:
            print(f"Terjadi error saat menghapus: {e}")

        print(f"\nSelesai. Total {count} pesan telah dihapus dari grup '{entity.title}'.")


# Menjalankan fungsi utama
if __name__ == "__main__":
    asyncio.run(main())
    