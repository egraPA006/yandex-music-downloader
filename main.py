import os
from yandex_music import Client
import help
from progress.bar import IncrementalBar

class app():
    token: str
    need_download = []
    need_remove = []
    my_playlist_name: str
    def run(self, token, playlist):
        self.token = token
        self.my_playlist_name = playlist
        self.connect()

    def connect(self):
        self.client = Client(self.token).init()
        self.check_updates()

    def check_updates(self):
        # Проверим есть ли папка music
        if not "music" in os.listdir():
            os.mkdir("music")
        # Собираем локальные треки
        old_tracks = []
        for track in os.listdir("music"):
            if track[-4:] == ".mp3":
                old_tracks.append(track[:-4])
        # Собираем серверные треки
        new_tracks = {}
        new_tracks_names = []
        # Находим нужный плейлист на сервере
        for playlist in self.client.users_playlists_list():
            if playlist.title == self.my_playlist_name:
                # Находим в нем треки
                for track in playlist.fetch_tracks():
                    new_tracks[f'{track.track.title} - {", ".join([artist.name for artist in track.track.artists])}'] = track.track
                    new_tracks_names.append(f'{track.track.title} - {", ".join([artist.name for artist in track.track.artists])}')

                self.need_download = list(set(new_tracks_names).difference(set(old_tracks)))
                self.need_remove = list(set(old_tracks).difference(set(new_tracks_names)))

                # Если нет изменений в плейлисте
                if len(self.need_download) == 0 and len(self.need_remove) == 0:
                    print("Изменений нет")
                    self.leave()
                
                # Запускаем скачивание новых треков
                for t_i in range(len(self.need_download)):
                    self.need_download[t_i] = new_tracks[self.need_download[t_i]]
                if len(self.need_download) != 0:
                    print(f"Будет скачано {len(self.need_download)} треков")
                    f = input("Начать скачивание (Y/n) или (Д/н): ")
                    if f == 'Y' or f == "Д" or f == "":
                        print("Скачивание")
                        self.download()
                        print("Сделанно")
                
                # Запускаем удаление старых треков
                if len(self.need_remove) != 0:
                    print(f"Будет удалено {len(self.need_remove)} треков")
                    f = input("Начать удаление (Y/n) или (Д/н): ")
                    if f == 'Y' or f == "Д" or f == "":
                        print("Удаление")
                        self.delete()
                        print("Сделанно")
                self.leave()
        print("У вас нет такого плейлиста")
        self.leave()

    def leave(self):
        # Выйти из программы
        exit()       
                    
    def download(self):
        bar = IncrementalBar('Скачано', max = len(self.need_download))
        for track in self.need_download:
            track.download(f'music/{track.title} - {", ".join([artist.name for artist in track.artists])}.mp3')
            bar.next()
        print()
    def delete(self):
        bar = IncrementalBar('Удалено', max = len(self.need_remove))
        for track in self.need_remove:
            os.remove(f"music/{track}.mp3")
            bar.next()
        print()

if __name__ == "__main__":
    prog = app()
    prog.run(token=help.token, playlist="...")
