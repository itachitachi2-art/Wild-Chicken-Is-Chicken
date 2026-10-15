Wild Chicken Is Chicken v0.1.3-test1
対象: 7 Days to Die v3.3（供給済みゲームDLLに対する互換ビルド）

今回は個別検査用です。ゲーム内での成功、投稿者の環境での解消はまだ確認していません。

変更
v0.1.2の処理をv3.3の実ゲーム参照で再ビルドしました。
v3.3のItemInventoryData.holdingEntityはfieldではなくpropertyになっているため、古いfield参照をgetter呼び出しへ置き換える必要があります。同名メンバーなので、C#のゲーム処理自体は変更せず、正しい参照での再ビルドで対応しています。
絞める操作、2秒バー、音、報酬、設定、レシピ、画像は変更していません。
起動ログはv0.1.3-test1、ModInfoは0.1.3で識別できます。

導入
1. ゲームを完全終了し、セーブと旧WildChickenIsChickenフォルダをバックアップ。
2. 本ZIP内のWildChickenIsChickenで旧フォルダを置き換える。新旧2個のMODや古いDLLを混在させない。
3. 7DTD v3.3をEAC無効で起動する。
4. ログの [WildChickenIsChicken] v0.1.3-test1 loaded を確認する。
5. 検査用セーブで下記を試す。

検査
・捕獲と運搬、鶏小屋への通常設置。
・セカンダリアクションを押して離し、2秒バーと音の後に絞めたニワトリ1個、羽23枚。
・バー途中で移動・持ち替えしても二重付与や消失がないこと。
・持ち替え後に元スロットが埋まっている場合と、インベントリ満杯時の付与/ドロップ。
・調理レシピ、セーブ/再読込。
・問題が続く場合は正確なゲームバージョン、MODの導入版、起動から例外までのログ、他のMOD一覧。

戻す場合はゲームを終了し、バックアップした旧MODに戻してください。実際に使うセーブは事前にバックアップしてください。

ビルド
ビルド済みDLL同梱のため通常は不要です。
build.cmd "D:\SteamLibrary\steamapps\common\7 Days To Die"
のように実際のv3.3インストール先を指定すると、Windows標準コンパイラで再ビルドできます。
v3.2参照でビルドすると再び旧API参照になります。バージョン表示だけでDLLの互換性を判断しないでください。
ゲーム本体のDLL・Harmonyは同梱しません。このMODはHarmonyパッチを登録しません。

確認済み
実ゲームDLLを参照したビルド成功。Assembly-CSharpの40メンバー参照が実メタデータと一致。
同じエラーを隔離テストで再現し、property APIに対する再ビルドで解消。
11項目の操作ロジック検査を旧/新の代替API各々で成功。

未確認
ゲーム内での音・描画・実インベントリ操作、投稿者の正確なDLL/ゲームビルド、マルチプレイ、専用サーバー、他MODとの互換性。
詳細は同梱VALIDATION.mdを参照してください。

English: This is a v3.3 compatibility test build. The compiled DLL is included.
Close the game, back up your save and existing mod, replace the old mod folder,
and test with EAC disabled on a disposable save. In-game validation is pending.
