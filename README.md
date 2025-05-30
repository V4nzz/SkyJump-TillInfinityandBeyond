# Froggie Jump

## Deskripsi Proyek
Froggie Jump adalah sebuah game platformer 2D di mana pemain mengendalikan karakter kodok yang melompat dari platform ke platform untuk mencapai skor tertentu dan menyelesaikan level. Game ini memiliki beberapa level dengan tingkat kesulitan yang berbeda-beda, platform dengan tipe yang bervariasi (normal, trampoline, fragile, moving), serta efek visual dan audio yang menarik untuk pengalaman bermain yang menyenangkan.

## Dependensi Paket
Untuk menjalankan game ini, Anda membutuhkan:
- Python 3.x
- Pygame (`pip install pygame`)
- Pillow (`pip install pillow`)

## Cara Menjalankan Aplikasi (Cara Bermain)
1. Pastikan semua dependensi telah terinstall.
2. Pastikan folder aset (gambar, musik, gif) tersedia di path yang benar sesuai dengan path dalam kode (atau sesuaikan path tersebut).
3. Jalankan file `Froggie-Jump.py` dengan perintah:
4. Pada menu utama, klik tombol "Play" untuk memulai level pertama.
5. Gunakan tombol panah kiri dan kanan untuk menggerakkan kodok ke kiri dan kanan.
6. Kodok akan otomatis melompat saat mendarat di platform.
7. Capai skor target untuk menyelesaikan level dan membuka level berikutnya.
8. Jika jatuh melewati bawah layar, permainan akan berakhir (game over).
9. Tekan tombol `R` saat bermain untuk merestart level.
10. Gunakan tombol `Escape` untuk kembali ke menu utama dari layar manapun.
11. Anda juga dapat memilih level melalui menu "Level Select" jika level sudah dibuka.

## UML Class Diagram
+------------------+
|      Game        |
+------------------+
| - state          |
| - level          |
| - player         |
| - platforms      |
| - raindrops      |
| - ...            |
+------------------+
| + update()       |
| + draw_menu()    |
| + draw_game()    |
| + handle_input() |
| + reset_game()   |
| + start_level()  |
+------------------+

      1
      |
      * 
+------------------+     +------------------+
|     Player       |     |    Platform      |
+------------------+     +------------------+
| - rect           |     | - rect           |
| - velocity_y     |     | - platform_type  |
| - is_jumping     |     | - move_direction |
| - ...            |     | - to_remove      |
+------------------+     +------------------+
| + update()       |     | + update()       |
| + find_closest_platform_above()| + break_platform() |
+------------------+     +------------------+

+------------------+
|    Raindrop      |
+------------------+
| - rect           |
| - speed          |
+------------------+
| + update()       |
+------------------+

## Kontributor Pengembangan Aplikasi
Ivan Nandira Mangunang (123140094)
Memory Simanjuntak (123140095)
Arsa Salsabila (123140108)
Grace Exauditha Nababan (123140115)
Fanisa Aulia Safitri (123140121)

## Referensi
Pou -- (Gameplay)
Growtopia -- (Asset Platform)
