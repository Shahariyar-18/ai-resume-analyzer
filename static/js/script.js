/* =========================================================
   AI RESUME ANALYZER - MAIN JAVASCRIPT
========================================================= */


/* =========================================================
   ELEMENTS
========================================================= */

const resumeInput =
    document.getElementById("resume");

const uploadBox =
    document.getElementById("uploadBox");

const uploadDefault =
    document.getElementById("uploadDefault");

const selectedFile =
    document.getElementById("selectedFile");

const fileName =
    document.getElementById("fileName");

const fileSize =
    document.getElementById("fileSize");

const chooseButton =
    document.getElementById("chooseButton");

const changeFile =
    document.getElementById("changeFile");

const analyzeBtn =
    document.getElementById("analyzeBtn");

const resumeForm =
    document.getElementById("resumeForm");



/* =========================================================
   FILE SELECTION
========================================================= */

if (resumeInput) {

    resumeInput.addEventListener(
        "change",
        function () {

            if (
                this.files &&
                this.files.length > 0
            ) {

                handleFile(
                    this.files[0]
                );

            }

        }
    );

}



/* =========================================================
   CHOOSE FILE BUTTON
========================================================= */

if (chooseButton) {

    chooseButton.addEventListener(
        "click",
        function (event) {

            event.stopPropagation();

            if (resumeInput) {

                resumeInput.click();

            }

        }
    );

}



/* =========================================================
   UPLOAD BOX CLICK
========================================================= */

if (uploadBox) {

    uploadBox.addEventListener(
        "click",
        function (event) {

            /*
             * Don't open the file picker
             * when clicking a button.
             */

            if (
                event.target.closest(
                    ".choose-button"
                )
                ||
                event.target.closest(
                    ".change-file"
                )
            ) {

                return;

            }


            if (resumeInput) {

                resumeInput.click();

            }

        }
    );

}



/* =========================================================
   CHANGE FILE BUTTON
========================================================= */

if (changeFile) {

    changeFile.addEventListener(
        "click",
        function (event) {

            event.stopPropagation();

            if (resumeInput) {

                resumeInput.click();

            }

        }
    );

}



/* =========================================================
   HANDLE FILE
========================================================= */

function handleFile(file) {

    if (!file) {
        return;
    }


    /* -----------------------------------------
       CHECK FILE TYPE
    ----------------------------------------- */

    const name =
        file.name.toLowerCase();


    const validPDF =
        name.endsWith(".pdf");


    const validDOCX =
        name.endsWith(".docx");


    if (
        !validPDF &&
        !validDOCX
    ) {

        alert(
            "Please upload a PDF or DOCX file."
        );

        if (resumeInput) {

            resumeInput.value = "";

        }

        return;

    }



    /* -----------------------------------------
       CHECK FILE SIZE
    ----------------------------------------- */

    const maxSize =
        10 * 1024 * 1024;


    if (file.size > maxSize) {

        alert(
            "File is too large. Maximum size is 10 MB."
        );

        if (resumeInput) {

            resumeInput.value = "";

        }

        return;

    }



    /* -----------------------------------------
       SHOW FILE NAME
    ----------------------------------------- */

    if (fileName) {

        fileName.textContent =
            file.name;

    }



    /* -----------------------------------------
       SHOW FILE SIZE
    ----------------------------------------- */

    if (fileSize) {

        fileSize.textContent =
            formatFileSize(
                file.size
            );

    }



    /* -----------------------------------------
       CHANGE UPLOAD STATE
    ----------------------------------------- */

    if (uploadBox) {

        uploadBox.classList.add(
            "file-selected"
        );

    }



    /* -----------------------------------------
       HIDE DEFAULT CONTENT
    ----------------------------------------- */

    if (uploadDefault) {

        uploadDefault.style.display =
            "none";

    }



    /* -----------------------------------------
       SHOW SELECTED FILE
    ----------------------------------------- */

    if (selectedFile) {

        selectedFile.style.display =
            "flex";

    }



    /* -----------------------------------------
       HIDE CHOOSE BUTTON
    ----------------------------------------- */

    if (chooseButton) {

        chooseButton.style.display =
            "none";

    }



    /* -----------------------------------------
       SHOW CHANGE BUTTON
    ----------------------------------------- */

    if (changeFile) {

        changeFile.style.display =
            "block";

    }

}



/* =========================================================
   FORMAT FILE SIZE
========================================================= */

function formatFileSize(bytes) {

    if (bytes < 1024) {

        return bytes + " B";

    }


    if (
        bytes <
        1024 * 1024
    ) {

        return (
            (bytes / 1024).toFixed(1)
            +
            " KB"
        );

    }


    return (
        (bytes / (1024 * 1024)).toFixed(1)
        +
        " MB"
    );

}



/* =========================================================
   DRAG & DROP
========================================================= */

if (uploadBox) {


    /* -----------------------------------------
       DRAG OVER
    ----------------------------------------- */

    uploadBox.addEventListener(
        "dragover",
        function (event) {

            event.preventDefault();

            uploadBox.classList.add(
                "drag-active"
            );

        }
    );


    /* -----------------------------------------
       DRAG LEAVE
    ----------------------------------------- */

    uploadBox.addEventListener(
        "dragleave",
        function () {

            uploadBox.classList.remove(
                "drag-active"
            );

        }
    );


    /* -----------------------------------------
       DROP
    ----------------------------------------- */

    uploadBox.addEventListener(
        "drop",
        function (event) {

            event.preventDefault();

            uploadBox.classList.remove(
                "drag-active"
            );


            const files =
                event.dataTransfer.files;


            if (
                files &&
                files.length > 0
            ) {

                const file =
                    files[0];


                /* Check extension */

                const name =
                    file.name.toLowerCase();


                if (
                    !name.endsWith(".pdf")
                    &&
                    !name.endsWith(".docx")
                ) {

                    alert(
                        "Please upload a PDF or DOCX file."
                    );

                    return;

                }


                /* Check size */

                const maxSize =
                    10 * 1024 * 1024;


                if (
                    file.size > maxSize
                ) {

                    alert(
                        "File is too large. Maximum size is 10 MB."
                    );

                    return;

                }


                /*
                 * Put dropped file into
                 * the real file input.
                 */

                try {

                    const dataTransfer =
                        new DataTransfer();


                    dataTransfer.items.add(
                        file
                    );


                    resumeInput.files =
                        dataTransfer.files;

                }
                catch (error) {

                    console.error(
                        "Could not assign dropped file:",
                        error
                    );

                }


                handleFile(file);

            }

        }
    );

}



/* =========================================================
   FORM SUBMIT
========================================================= */

if (resumeForm) {

    resumeForm.addEventListener(
        "submit",
        function (event) {


            /* -----------------------------------------
               MAKE SURE FILE EXISTS
            ----------------------------------------- */

            if (
                !resumeInput
                ||
                !resumeInput.files
                ||
                resumeInput.files.length === 0
            ) {

                event.preventDefault();

                alert(
                    "Please select a resume first."
                );

                return;

            }



            /* -----------------------------------------
               DISABLE BUTTON
            ----------------------------------------- */

            if (analyzeBtn) {

                analyzeBtn.disabled =
                    true;


                analyzeBtn.classList.add(
                    "loading"
                );


                analyzeBtn.innerHTML =
                    `
                    <span>
                        Analyzing Resume...
                    </span>

                    <span>
                        ⏳
                    </span>
                    `;

            }

        }
    );

}



/* =========================================================
   COPY RESUME TEXT
   Used on result.html
========================================================= */

function copyResumeText() {

    const textArea =
        document.getElementById(
            "resumeText"
        );


    if (!textArea) {

        return;

    }


    navigator.clipboard
        .writeText(
            textArea.value
        )
        .then(
            function () {

                const button =
                    document.querySelector(
                        ".copy-button"
                    );


                if (!button) {

                    return;

                }


                const original =
                    button.textContent;


                button.textContent =
                    "✓ Copied";


                setTimeout(
                    function () {

                        button.textContent =
                            original;

                    },
                    1500
                );

            }
        )
        .catch(
            function () {

                /*
                 * Fallback for browsers
                 * that block clipboard API.
                 */

                textArea.select();

                document.execCommand(
                    "copy"
                );

            }
        );

}



/* =========================================================
   NUMBER COUNTER
   Used on result.html
========================================================= */

const counters =
    document.querySelectorAll(
        ".counter"
    );


counters.forEach(
    function (counter) {

        const target =
            parseFloat(
                counter.dataset.target
            );


        if (
            isNaN(target)
        ) {

            return;

        }


        let current = 0;


        const increment =
            target / 40;


        const updateCounter =
            setInterval(
                function () {

                    current +=
                        increment;


                    if (
                        current >=
                        target
                    ) {

                        counter.textContent =
                            target;


                        clearInterval(
                            updateCounter
                        );

                    }
                    else {

                        counter.textContent =
                            Math.floor(
                                current
                            );

                    }

                },
                25
            );

    }
);