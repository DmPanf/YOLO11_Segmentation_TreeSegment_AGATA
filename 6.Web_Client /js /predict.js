    async function predict() {
        if (!originalImage.src) {
            console.error("No image selected.");
            return;
        }

        // Отправить оригинальное изображение на сервер для сегментации
        const formData = new FormData();
        formData.append("image", dataURLtoFile(originalImage.src, "input.png"));

        try {
            const response = await fetch("http://51.250.26.141/process_image", {
                method: "POST",
                body: formData
            });

            if (!response.ok) {
                throw new Error(`HTTP error ${response.status}`);
            }

            // Получить сегментированное изображение и установить его как src у segmentedImage
            const blob = await response.blob();
            const blobUrl = URL.createObjectURL(blob);
            segmentedImage.src = blobUrl;
            downloadLink.href = blobUrl;
        } catch (error) {
            console.error(error);
        }
    }
