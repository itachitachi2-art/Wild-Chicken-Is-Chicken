Wild Chicken Is Chicken v0.1.2
Wild chickens are chickens. Catch it. Raise it. Or eat it.
対象 / Target: 7 Days to Die v3.2

導入
1. DLL入りZIPは展開後そのまま導入できます。ソースZIPや再ビルドでは最上位のbuild.cmdをダブルクリックしてください。
   Windows標準の.NET Framework C#コンパイラを使用します。.NET SDKは不要です。
2. WildChickenIsChickenフォルダを普段使用しているModsへコピーしてください。再ビルド時はBUILD OKを確認してください。
3. EACを無効にして起動してください。
更新時はゲームを完全終了して旧MODフォルダと置き換えてください。
ゲームを自動検出できない場合:
  build.cmd "D:\SteamLibrary\steamapps\common\7 Days To Die"
GitHubのソースZIPにコンパイル済みDLLは同梱していません。ソースからの導入では初回のビルドが必要です。
ゲーム本体のDLL・Harmonyは同梱しません。このMODはHarmonyを必要としません。

DLL入りZIPの作成
最上位のbuild-release.cmdを実行してください。
ビルド成功後にWildChickenIsChicken-v0.1.2-install.zipを生成します。
生成されたZIPは展開したMODフォルダをModsへ入れるだけで導入できます。

操作と内容
・野生鶏を従来どおり捕獲します。
・飼う場合: 抱えて鶏小屋へ運びます。
・食べる場合: 抱えた状態でセカンダリアクション（標準右クリック）を押して離します。
・約2秒の装飾用バーが進み、終了時に鶏の鳴き声が再生されてから絞めたニワトリ1個と羽23枚を得ます。
・鶏は受付時に一羽消費します。バー表示中も移動や持ち替えができ、操作によるキャンセルはありません。
・元の手持ち枠が他のアイテムで埋まった場合、絞めたニワトリはインベントリへ入り、満杯なら地面へ落ちます。
・絞めたニワトリは元の手持ち枠へ入ります。入りきらない羽は地面へ落ちます。
・絞めたニワトリは手羽先、アッシュチキンシチュー、ロードランナー・チキンジャーキーに使用できます。
・絞めたニワトリを鶏小屋で飼うことはできません。
・野生鶏の逃走設定MoveSpeedPanicを1.5から1.2へ調整します。
・通常の狩猟・鶏小屋の餌や生産設定・チキンナゲットのレシピは変更しません。
・表示名は日本語「絞めたニワトリ」、英語「Butchered Chicken」。説明文も日英対応です。

Installation
Extract this package, run build.cmd, then copy the built WildChickenIsChicken
folder into your Mods directory. Disable EAC. No .NET SDK is required.
To generate a ready-to-install ZIP containing the compiled mod DLL, run build-release.cmd.
While carrying a captured chicken, press and release the secondary action
(default right mouse button) to obtain one Butchered Chicken and 23 feathers.
A decorative two-second progress bar finishes, then the chicken sound is requested
before either item reward is granted. The live chicken is consumed on acceptance.
Moving or switching items does not cancel the presentation.
Feathers that do not fit in the inventory drop on the ground.
Carry live chickens to the coop as usual to raise them.

確認状況 / Known status
今回追加した2秒バー・鳴き声・音の後の付与は実機未確認。
捕獲・運搬・絞める操作・料理への利用はユーザー実機確認済み。羽の採取も確認済み。
修正後の専用アイコン表示と鶏小屋の継続生産もユーザー実機確認済み。
満杯時の羽ドロップの個別確認は未報告。
マルチプレイ・専用サーバー・他の鶏料理MODとの互換性は未確認です。
「ミープ！ミープ！」表示の報告は原因未確定のため保留しています。
