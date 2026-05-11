# au lieu de FROM golang:1.18 ou similaire
FROM golang:1.25-alpine AS builder
# ...

# au lieu d'une image de base ancienne
FROM oraclelinux:9-slim
# ou mieux : une image distroless/alpine récente
