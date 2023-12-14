# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [v1.1.0] - 2023-12-14

### Added
- feat: add dead-simple frontend using React

### Changed
- refactor: enhance repository structure
- docs: improve changelog
- refactor: install lgm-prices in aws lambda from main branch instead of dev

### Fixed
- refactor: removed sensitive data from repository using BFG
- fix: merge seller's name without logo hotfix

## [v1.0.1] - 2022-12-30

### Fixed
- fix: extract seller name that do not have image logo and has div with clas "mp-loja-semlogo"

## [v1.0.0] - 2022-10-16

### Added
- feat: python package 'lgm-prices' with methods to scrappe data from LigaMagic's marketplace
- feat: create aws lambda resource using 'lgm-prices' packages to scrappe data on-demand using lambda rest api

