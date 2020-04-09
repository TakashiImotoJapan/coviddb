
COVID-19 DATABASE
====

## 概要

COVID-19のデータベースサイトであるCOVID-19 DATABASE（http://covid19db.info/）のソースコードです。

COVID-19 DATABASEは、研究者やデータサイエンティストが分析に利用できるデータベースの構築を行う事を目的に開発しました。

## 設立趣旨

今、新型コロナウイルスに関し世の中では、データや数理的分析など論理的整理にされたものに基づいものでなく、感想や予想が多く、ほとんどが感覚的なものや感情的な話が溢れています。

では、AIなどで分析し何らかの知見を得ればいいのではないかということに思い至る方は多いかと思います。
しかし、AIなどで分析しようにもデータがなく、それをどうつくるかで必ず壁にあたり、既に難航しています。
このような状況に鑑み、その壁を乗り越えるべく、様々な人材が協調して、新型コロナウイルス(COVID-19)オープンデータベースをつくろうという伊本貴士氏の高志をもとに、まず氏がDBを作成し始めました。（その発足を訴える2020.4.9 12:46の投稿・コメントを別途閲覧ください）

現在この人類の敵に対する対処は世界の喫緊の課題であり、一刻も早い根本的解決を求められています。
それには、①このウイルスのデータを集め、②AIなどの帰納的分析により有用な知見を得なければなりません。
①に関しては、このデータベースをオープンにし様々なタレント・団体企業の参加を促すとともに、かつ、可能な限りスピーディに早く構築を成し遂げなければなりません。既に伊本氏はこのデータベースのβ版をつくり上げて公開してします。
②については、分析を可及的速やかに行うための言語プログラムレスAI開発環境の無償提供も申し出られています。

このような趣旨に賛同いただき参加していただける方を歓迎いたします。

新型コロナウイルスに対する解決知見の探究をきっかけに、データ分析で賢く判断するということを日本でも認知させていきたいとも思っています。

## 開発環境

Python 3.8.2

Diango 3.0.5

## ダッシュボードテンプレート

WebのJavascriptおよびCSSには、AdminLTE3を利用しています。

https://adminlte.io/themes/dev/AdminLTE/index.html

グラフや地図などの表示部分は、ほぼAdminLTE3を見ればわかります。

AdminLTE3のベースはBootStrap4です。

## ローカル環境の構築

gitでクローンした上で、djangoの起動をすれば動くと思います。
manage.pyは、トップディレクトリ直下にあります。

## データの入力について

新型コロナウイルスの感染者は日々増える一方です。
その上で、データ入力が追いついておりません。
世界への貢献のため、データ入力への貢献をお願いします。

データ仕様および作成方法については、
https://github.com/TakashiImotoJapan/coviddb/README_DATABASE.md
を参照してください。

## このプロジェクトへの貢献

現在、仮でFacebookグループにて、情報発信および交換を行っております。
https://www.facebook.com/groups/218786599431322/

後々には、だれでも参加可能な形に移行したいと思いますが、とりあえずはここでお願いします。

それ以外で、なにかある場合はinfo@media-sketch.comまで連絡をお願いします。
（多忙のため、返事が遅い場合があります。）

バグの報告はFacebookグループまたは、info@media-sketch.comまでお願いします。

## ライセンスについて

このソースコードは、MIT Licenseに基づき公開されています。
[MIT](https://github.com/tcnksm/tool/blob/master/LICENCE)

利用は無償で問題ありませんが、著作権表示および本許諾表示をソフトウェアのすべての複製または重要な部分に記載する必要があります。

データに関しては、クリエイティブコモンズライセンス(CC BY 4.0)に基づき公開されています。
利用に関しては、著作権表示が必要になります。
著作権表示をすれば、誰でも利用可能です。
データを商業目的に販売、利用する事は原則禁止とします。

データおよび分析結果を著作権表示を行った上でメディア等に掲載する事は可能です。

不明な場合は、info@media-sketch.comまでお問い合わせください。

## Author

[COVID-19 DATABASE](https://github.com/TakashiImotoJapan/coviddb)