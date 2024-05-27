# Changelog

## [0.5.0](https://github.com/Mouwrice/DrumPy/compare/v0.4.0...v0.5.0) (2024-05-27)


### Features

* process results ([5835dc5](https://github.com/Mouwrice/DrumPy/commit/5835dc5202f37873f098424d0e12f4302ae4e7d1))


### Bug Fixes

* fix audio files ([9e66b8f](https://github.com/Mouwrice/DrumPy/commit/9e66b8ff13a395fbdbf7b9d468a71af12f7fb643))

## [0.4.0](https://github.com/Mouwrice/DrumPy/compare/v0.3.0...v0.4.0) (2024-05-14)


### Features

* the drumming model now uses the NormalizedLandmark instead of the World Landmarks for increased stability ([998a861](https://github.com/Mouwrice/DrumPy/commit/998a861808100bc8683e280fab9edbb636d0f48d))


### Bug Fixes

* **deps:** update dependency mediapipe to v0.10.14 ([#52](https://github.com/Mouwrice/DrumPy/issues/52)) ([4dd72e6](https://github.com/Mouwrice/DrumPy/commit/4dd72e6cbf475935d831ccc16af2eab742c15e4b))

## [0.3.0](https://github.com/Mouwrice/DrumPy/compare/v0.2.1...v0.3.0) (2024-05-03)


### Features

* improve tracking and drum ([6d6a07d](https://github.com/Mouwrice/DrumPy/commit/6d6a07dfc787931d6abc8bcb07f3caab62ebdb86))


### Bug Fixes

* .task files path ([77361f6](https://github.com/Mouwrice/DrumPy/commit/77361f6cd3afecaa1fcd0c61669747209382388d))
* fix camera input axis transformation and improve hit detection ([7665f5f](https://github.com/Mouwrice/DrumPy/commit/7665f5fa7e42c509ae4a301773e7f0f25466bee0))
* fix corrupt audio file ([b656121](https://github.com/Mouwrice/DrumPy/commit/b65612101a691d1227f2b89266e545c202023633))

## [0.2.1](https://github.com/Mouwrice/DrumPy/compare/v0.2.0...v0.2.1) (2024-04-27)


### Bug Fixes

* docs ([bfb86a0](https://github.com/Mouwrice/DrumPy/commit/bfb86a0342caeed2d36f748707dfb48e3844ecb2))

## [0.2.0](https://github.com/Mouwrice/DrumPy/compare/v0.1.1...v0.2.0) (2024-04-26)


### Features

* add basic drums and auto fine tuning ([9653f24](https://github.com/Mouwrice/DrumPy/commit/9653f244cfb8660dd5ae065bf459f6230d6dc4e9))
* add drum back ([de38177](https://github.com/Mouwrice/DrumPy/commit/de3817793984798ca07988fdd7fb2ceb1042f4f2))
* add hit aggregation and improve drum position ([61193de](https://github.com/Mouwrice/DrumPy/commit/61193de84ff6b3d9c6abf57312ea7e65d078b8f5))
* add pygame gui ([b22be4a](https://github.com/Mouwrice/DrumPy/commit/b22be4af2d5bfd26132ba7c3b255ad13b036656b))
* async detection and latency graph ([ab2fe41](https://github.com/Mouwrice/DrumPy/commit/ab2fe410f3d7fb9ab978b52211149e2f5572264f))
* blocking mode ([368b889](https://github.com/Mouwrice/DrumPy/commit/368b88962ca59e88909f7a1f5292618e7d868a4a))
* build linux binary script ([fa4fbc9](https://github.com/Mouwrice/DrumPy/commit/fa4fbc9a01be0269ffe7409ef65802f50f4d8c04))
* built exe ([cfb046d](https://github.com/Mouwrice/DrumPy/commit/cfb046d1599fb97ec0cb4c8e612261652ef0d24a))
* cli ([7a7cacb](https://github.com/Mouwrice/DrumPy/commit/7a7cacb53abcba28d0b719f9af0a04dc6fa33419))
* first measurements and comparison start ([0fd1176](https://github.com/Mouwrice/DrumPy/commit/0fd11762b14aa38ff5e948e1b38cfe925dd32249))
* fix performance issues ([8546967](https://github.com/Mouwrice/DrumPy/commit/854696722e3e7a0f7702358a11ad07807c38909e))
* fix plotting ([893fb1c](https://github.com/Mouwrice/DrumPy/commit/893fb1cbf9ece9c62a1f41a58ef8c3bd38824ec0))
* improve calibration and output formatting ([2345318](https://github.com/Mouwrice/DrumPy/commit/2345318ccbec3ce7925b0171739c10fa21c2aa76))
* improve graph ([3fc264f](https://github.com/Mouwrice/DrumPy/commit/3fc264f4fd5e1e59f1781f3962e2a23dc8b4793b))
* improve logging, disable sleep ([6085f12](https://github.com/Mouwrice/DrumPy/commit/6085f12414f71b4b64b4375a1fea005334eeed5d))
* improved mediapipe logging ([aee9db1](https://github.com/Mouwrice/DrumPy/commit/aee9db13f9bb96006b096258b874ceff25be84f0))
* init result processor ([a27bfe8](https://github.com/Mouwrice/DrumPy/commit/a27bfe8e7fefb897e7a4dd5bb38c036c58566c19))
* interpolate between predicted and actual landmark position ([0cc5fa6](https://github.com/Mouwrice/DrumPy/commit/0cc5fa674d07efed3df817151fcb78566bfe6bf0))
* landmark graphs ([498a059](https://github.com/Mouwrice/DrumPy/commit/498a0594b6901aa0588a2fc86cf06fe30a51cdc1))
* live option ([39cb956](https://github.com/Mouwrice/DrumPy/commit/39cb956fcecd07ba88c462c9479c3b2f45d0d6c4))
* log all available data ([4162541](https://github.com/Mouwrice/DrumPy/commit/4162541e0cfcbc48cc4e1bac934fb1fd3e92273c))
* loggin to csv file ([24a0098](https://github.com/Mouwrice/DrumPy/commit/24a009885fa3321b628256eb4fcbfc0bd96ef3f4))
* mediapipe pose tracking and visualisation ([8da69f7](https://github.com/Mouwrice/DrumPy/commit/8da69f7aadf383436f481d3e88771dde3c9975de))
* multiprocessing for graphs ([cffaae0](https://github.com/Mouwrice/DrumPy/commit/cffaae09f20eb4220c617a42835d3d5c82cf02ef))
* new measurement setup ([4c8b134](https://github.com/Mouwrice/DrumPy/commit/4c8b1348b3c91039693273a2b2c8cc8c1464ffc3))
* normalized landmarks and improved output ([1483969](https://github.com/Mouwrice/DrumPy/commit/1483969ee818eebf3abaecc514ef38c97ba0d0eb))
* normalized vs world coords ([b4abab9](https://github.com/Mouwrice/DrumPy/commit/b4abab9f1c1fb135f64fd191830a36786e1f0d52))
* parameter fine tuning ([c83350e](https://github.com/Mouwrice/DrumPy/commit/c83350eb103203cfd13d001a11df267c446d504b))
* plot multicam 1 left ([5b2c502](https://github.com/Mouwrice/DrumPy/commit/5b2c5022361b09e0ed285179bb54185c7e88255b))
* plotting ([1ec95e4](https://github.com/Mouwrice/DrumPy/commit/1ec95e4a30af6f9cd9f34fcbf6655670dc495d37))
* plotting ([37211c8](https://github.com/Mouwrice/DrumPy/commit/37211c81e87ebeadd0507376c90a2828637067f8))
* predict and smooth results ([9dc8611](https://github.com/Mouwrice/DrumPy/commit/9dc8611357221844ec8ecdacfb5ead9874d37a68))
* qtm label to marker enum ([d4912ba](https://github.com/Mouwrice/DrumPy/commit/d4912babb3b880d87ef9d109b9e222e446fd64e8))
* refactor ([12252d4](https://github.com/Mouwrice/DrumPy/commit/12252d41fe3dc0bcaa1d694756f3861d090ac7b7))
* resizeble camera display ([2649c02](https://github.com/Mouwrice/DrumPy/commit/2649c0239d793a33deeadacd91e6d01034619711))
* resolution and model plots ([38761eb](https://github.com/Mouwrice/DrumPy/commit/38761ebfd4966ffa2a3e6a9971769f02c81fc47d))
* some calibrations ([b6edeea](https://github.com/Mouwrice/DrumPy/commit/b6edeeac07ea67f1e964afd08c26138c84ae95f0))
* square input ratio ([2777a3c](https://github.com/Mouwrice/DrumPy/commit/2777a3c50d7c034ddf88453d0cab895209b9649c))
* start implementing tracking using mediapipe and calibration ([38b37db](https://github.com/Mouwrice/DrumPy/commit/38b37dbb5d56d58ab50dd648bda380854c97caba))
* stream and write qtm packets to csv ([bafd5be](https://github.com/Mouwrice/DrumPy/commit/bafd5be783ae35166dad9b1365c4e5a0be86653a))
* ui cleanup ([c3b781e](https://github.com/Mouwrice/DrumPy/commit/c3b781e282fc867f58d96f8bd31d89c0bd44bd4c))
* ui fps display ([90c436d](https://github.com/Mouwrice/DrumPy/commit/90c436d51ef6fb52f0c492875ffd9e3df62cb634))
* very basic working prototype ([6bc5a5f](https://github.com/Mouwrice/DrumPy/commit/6bc5a5f82421e7122d4d5d2c98c572101d16529b))
* visualize landmarks ([b6feea7](https://github.com/Mouwrice/DrumPy/commit/b6feea7db770fb50d90e37f203161a60b730796b))


### Bug Fixes

* apply ruff warnings ([0fc0cfc](https://github.com/Mouwrice/DrumPy/commit/0fc0cfce6c2bce154c56664e536e6cb963782c9b))
* ci permissions ([8ff0731](https://github.com/Mouwrice/DrumPy/commit/8ff0731b32cff55c94b7961e4ba372c461feefd6))
* delete unneeded resources ([1a4a465](https://github.com/Mouwrice/DrumPy/commit/1a4a46546bc93393b683d937e08881c957b21d21))
* **deps:** update dependency mediapipe to v0.10.11 ([#6](https://github.com/Mouwrice/DrumPy/issues/6)) ([36fd6fa](https://github.com/Mouwrice/DrumPy/commit/36fd6fa04c4361574ad9bcfcad9b7a12b5b7cbb4))
* **deps:** update dependency pygame-gui to v0.6.10 ([#36](https://github.com/Mouwrice/DrumPy/issues/36)) ([a268e7e](https://github.com/Mouwrice/DrumPy/commit/a268e7e548dcd581bc9b43b322d059c894951f4a))
* **deps:** use poetry build system ([e8f7230](https://github.com/Mouwrice/DrumPy/commit/e8f72308161b0fa58296607427febdb21f6eb455))
* distance was not the distance but a boolean ([cb9f124](https://github.com/Mouwrice/DrumPy/commit/cb9f1242038b8ee33d552f9ccff0b6ec456238ec))
* fix merge issue ([60ea042](https://github.com/Mouwrice/DrumPy/commit/60ea042274c1d59a8213638e2c38c6923c63fa2d))
* fix refactor issues ([4bed9dd](https://github.com/Mouwrice/DrumPy/commit/4bed9ddb551fffc511b1779aec962c996b7a17c6))
* fix writing to file ([bd9ee9a](https://github.com/Mouwrice/DrumPy/commit/bd9ee9a032fdc344f15b2de408e84fbbaef10672))
* fixed naming scheme ([6cf3fc5](https://github.com/Mouwrice/DrumPy/commit/6cf3fc50c81888848516a1e3630f10f0e8b91b6d))
* intellij stuff ([f93571c](https://github.com/Mouwrice/DrumPy/commit/f93571c58e588dbb5a080055e74316a45fd4dd16))
* processing ([c513005](https://github.com/Mouwrice/DrumPy/commit/c5130056ff44817c7052019cad088b723fad4f39))
* prune deps ([cb583cd](https://github.com/Mouwrice/DrumPy/commit/cb583cda97afcd65b098bfd6141890315457f998))
* upload to release ([84ec35c](https://github.com/Mouwrice/DrumPy/commit/84ec35c06c733c83a3ab4be709bec3eeeb564eab))
* use absolute imports and create left side data ([90adf80](https://github.com/Mouwrice/DrumPy/commit/90adf80e173c151f5b3f782ba77d568ba0df33b6))


### Dependencies

* poetry lock ([dfd83aa](https://github.com/Mouwrice/DrumPy/commit/dfd83aafef2823491e8985a66c16c3f05c439657))


### Documentation

* readme ([ee4b67c](https://github.com/Mouwrice/DrumPy/commit/ee4b67cff508d9ab0cc4d78f2eb3f12648702e38))
* update installation guide ([e93c405](https://github.com/Mouwrice/DrumPy/commit/e93c40578544ad43190a6189e213828f8d5fb4b3))

## [0.1.1](https://github.com/Mouwrice/DrumPy/compare/v0.1.0...v0.1.1) (2024-04-26)


### Bug Fixes

* ci permissions ([8ff0731](https://github.com/Mouwrice/DrumPy/commit/8ff0731b32cff55c94b7961e4ba372c461feefd6))
* delete unneeded resources ([1a4a465](https://github.com/Mouwrice/DrumPy/commit/1a4a46546bc93393b683d937e08881c957b21d21))
* upload to release ([84ec35c](https://github.com/Mouwrice/DrumPy/commit/84ec35c06c733c83a3ab4be709bec3eeeb564eab))

## [0.1.0](https://github.com/Mouwrice/DrumPy/compare/v0.0.1...v0.1.0) (2024-04-24)


### Features

* add drum back ([de38177](https://github.com/Mouwrice/DrumPy/commit/de3817793984798ca07988fdd7fb2ceb1042f4f2))
* build linux binary script ([fa4fbc9](https://github.com/Mouwrice/DrumPy/commit/fa4fbc9a01be0269ffe7409ef65802f50f4d8c04))
* cli ([7a7cacb](https://github.com/Mouwrice/DrumPy/commit/7a7cacb53abcba28d0b719f9af0a04dc6fa33419))
* init result processor ([a27bfe8](https://github.com/Mouwrice/DrumPy/commit/a27bfe8e7fefb897e7a4dd5bb38c036c58566c19))
* interpolate between predicted and actual landmark position ([0cc5fa6](https://github.com/Mouwrice/DrumPy/commit/0cc5fa674d07efed3df817151fcb78566bfe6bf0))
* normalized vs world coords ([b4abab9](https://github.com/Mouwrice/DrumPy/commit/b4abab9f1c1fb135f64fd191830a36786e1f0d52))
* parameter fine tuning ([c83350e](https://github.com/Mouwrice/DrumPy/commit/c83350eb103203cfd13d001a11df267c446d504b))
* predict and smooth results ([9dc8611](https://github.com/Mouwrice/DrumPy/commit/9dc8611357221844ec8ecdacfb5ead9874d37a68))
* qtm label to marker enum ([d4912ba](https://github.com/Mouwrice/DrumPy/commit/d4912babb3b880d87ef9d109b9e222e446fd64e8))
* square input ratio ([2777a3c](https://github.com/Mouwrice/DrumPy/commit/2777a3c50d7c034ddf88453d0cab895209b9649c))


### Bug Fixes

* **deps:** update dependency pygame-gui to v0.6.10 ([#36](https://github.com/Mouwrice/DrumPy/issues/36)) ([a268e7e](https://github.com/Mouwrice/DrumPy/commit/a268e7e548dcd581bc9b43b322d059c894951f4a))
* **deps:** use poetry build system ([e8f7230](https://github.com/Mouwrice/DrumPy/commit/e8f72308161b0fa58296607427febdb21f6eb455))
* fix refactor issues ([4bed9dd](https://github.com/Mouwrice/DrumPy/commit/4bed9ddb551fffc511b1779aec962c996b7a17c6))
* fix writing to file ([bd9ee9a](https://github.com/Mouwrice/DrumPy/commit/bd9ee9a032fdc344f15b2de408e84fbbaef10672))
* intellij stuff ([f93571c](https://github.com/Mouwrice/DrumPy/commit/f93571c58e588dbb5a080055e74316a45fd4dd16))
* processing ([c513005](https://github.com/Mouwrice/DrumPy/commit/c5130056ff44817c7052019cad088b723fad4f39))
