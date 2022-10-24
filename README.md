# README

Macに接続した外部ストレージの特定のフォルダ内のNikonで撮影した画像ファイルについて、
バーコードの番号にリネームする

## 撮影方法
1. 対象の服を取る前にバーコードを撮影する
2. 対象の服をとる(複数枚OK)
3. 別の服を撮影する場合1に戻りバーコードを撮影する

## 利用方法
1. 外部ストレージをMacに接続する
2. 以下コマンドを実行し、対象のストレージのディスクIDを取得する
    ```
    diskutil list
    ```
    `disk3s1` みたいなのがディスクID

2. 以下のコマンドをこのディレクトリ配下で実行
    ```
    sh mount.sh ${ストレージID} ${ディスクID} mount
    ```
    - これにより、Windows用にNTFSでフォーマットされた外部ストレージも書き込める
    - ストレージIDは、外部ストレージごとに設定・登録する。設定方法は別項目で
3. 以下コマンドを実行する
    ```
    docker-compose run --rm remake_image python main.py ${ストレージID}/${対象のフォルダのパス}
    ```
    - 対象のフォルダのパスは、外部ストレージのトップからの相対パス
        - /Volumes/{ストレージID}/{対象のフォルダパス}
    - ex) 対象フォルダが外部ストレージ(`hpdc`)の `画像/20220101` だった場合
        ```
        docker-compose run --rm remake_image python main.py hdpc/画像/20220101
        ```
4. `volume_link` は 外部ストレージのシンボリックリンクなので、そこから対象のフォルダがリネームされていることを確認する

5. 以下コマンドを実行し、外部ストレージを取り外す(必ず取り外す)
    ```
    sh mount.sh ${ストレージID} mount
    ```

## 環境構築
### Dockerの構築
1. dockerを入れる
2. 以下を実行
    ```
    docker-compose build
    ```

### 外部ストレージ情報の登録
このスクリプトは、外部ストレージごとに設定が必要となる
(Macの認識した情報をもとにマウントするため)
1. 外部ストレージを接続する
2. `diskutil list` を実行し、以下のような情報をえる
    ```
    /dev/disk2 (external, physical):
    #:     TYPE NAME                    SIZE       IDENTIFIER
    0:     FDisk_partition_scheme       *1.0 TB     disk2
    1:     Windows_NTFS HDPC-UT          1.0 TB     disk2s1
    ```
    上記の例では
    - ストレージの名前: `HDPC-UT`
    - ディスクの名前: `disk2s1`

    となる
3. 任意のストレージIDを決める(上の例では `hdpc` とする)
4. mount.shを以下の形でif分岐を追加する
    ```
    elif [ $1 == {ストレージID} ]; then
        if [ $2 == 'mount' ]; then
            sudo umount /Volumes/{ストレージの名前}
            sudo mkdir /Volumes/{ストレージID}
            sudo mount -t ntfs -o nobrowse,rw /dev/{ディスクの名前} /Volumes/{ストレージID}
            ln -s /Volumes/{ストレージID} ./volumes_link/{ストレージID}
        elif [ $2 == 'umount' ]; then
            sudo umount /Volumes/{ストレージID}
            rm ./volumes_link/{ストレージID}
        fi
    ```
5. docker-compose.yml でマウントするボリュームを追加する
    ```
    - type: bind
        source: "/Volumes/{ストレージID}"
        target: "/src/volumes/{ストレージID}"
    ```




# object_fit_images
