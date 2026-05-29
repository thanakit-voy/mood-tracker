(function () {
  const form = document.getElementById("mood-form");
  const modal = document.getElementById("quote-modal");
  const modalEmoji = document.getElementById("modal-emoji");
  const modalQuote = document.getElementById("modal-quote");
  const formError = document.getElementById("form-error");
  const submitBtn = document.getElementById("submit-btn");
  const messageInput = document.getElementById("message");
  const charCurrent = document.getElementById("char-current");

  function setMoodTheme(mood) {
    if (mood) {
      document.body.dataset.mood = mood;
    }
  }

  function showError(msg) {
    formError.textContent = msg;
    formError.hidden = false;
  }

  function hideError() {
    formError.hidden = true;
  }

  function openModal(emoji, quote) {
    modalEmoji.textContent = emoji;
    modalQuote.textContent = quote;
    modal.hidden = false;
    modal.setAttribute("aria-hidden", "false");
    document.body.style.overflow = "hidden";
  }

  function closeModal() {
    modal.hidden = true;
    modal.setAttribute("aria-hidden", "true");
    document.body.style.overflow = "";
  }

  function setLoading(loading) {
    submitBtn.disabled = loading;
    submitBtn.classList.toggle("loading", loading);
  }

  if (messageInput && charCurrent) {
    messageInput.addEventListener("input", () => {
      charCurrent.textContent = messageInput.value.length;
    });
  }

  document.querySelectorAll("[data-close-modal]").forEach((el) => {
    el.addEventListener("click", closeModal);
  });

  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape" && !modal.hidden) {
      closeModal();
    }
  });

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    hideError();

    const mood = form.querySelector('input[name="mood"]:checked')?.value;
    const activity = form.querySelector('input[name="activity"]:checked')?.value;
    const message = messageInput.value.trim();

    if (!mood) {
      showError("Please pick a mood!");
      return;
    }
    if (!activity) {
      showError("Please pick an activity!");
      return;
    }
    if (!message) {
      showError("Please write a message!");
      return;
    }

    setLoading(true);

    try {
      const res = await fetch("/api/generate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ mood, activity, message }),
      });

      const data = await res.json();

      if (!res.ok) {
        showError(data.error || "Something went wrong. Try again!");
        return;
      }

      setMoodTheme(data.mood);
      openModal(data.mood_emoji, data.quote);
    } catch {
      showError("Could not connect. Check your internet and try again!");
    } finally {
      setLoading(false);
    }
  });
})();
