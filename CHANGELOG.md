# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [v1.0.1] - 2022-12-30

### Fixed
- fix: Extract seller name that do not have image logo and has div with clas "mp-loja-semlogo"

## [v1.0.0] - 2022-10-16

### Added
- Add data module with esparac true font for image preprocessing
- Add utils module with general routines
- Add marketplace module with class to open card in ligamagic marketplace and extract inventory information and price css codes
- Add image submodule with PriceRecognizer class in order to recognize price numbers as string from assets file
- Add card submoule to access card's information in inventory html
- Add repoUri file with ECR repository path to register lambda container
- Add get_card lambda function to access ligamagic and get card inventory (with prices using OCR) on demand
- Add sam template, build and deploy scripts
- Add custom LambdaRole in sam template and add project:deploy-stage tag in FetchCardLGMFunction resource

### Changed
- Improve get_card dockerfile to reduce container memory size
- Change tesseract-ocr language pack from tessdata_fast to tessdata to improve detection performance
