ARG WAHA_IMAGE=devlikeapro/waha:latest

FROM ${WAHA_IMAGE}

# Railway specific environment
ENV WAHA_PRINT_QR=true \
    WAHA_LOG_LEVEL=info \
    PORT=3000

EXPOSE 3000

# Use default WAHA entrypoint
CMD ["node", "dist/main"]
