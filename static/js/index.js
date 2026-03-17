const resultGroups = {
  self: {
    overline: "Expression-driven animation",
    title: "Self-Reenactment",
    description:
      "Subject-specific self-reenactment sequences illustrating how facial appearance details are preserved under expression-driven animation.",
    featured: {
      src: "videos/self_reeactment/1.mp4",
      title: "Representative self-reenactment sequence",
      subtitle: "Qualitative sequence"
    },
    items: Array.from({ length: 9 }, (_, index) => ({
      src: `videos/self_reeactment/${index + 1}.mp4`,
      title: `Self Reenactment ${index + 1}`,
      subtitle: "Qualitative sequence"
    }))
  },
  cross: {
    overline: "Cross-subject driving",
    title: "Cross-Reenactment",
    description:
      "Cross-reenactment sequences demonstrating target-avatar rendering under driving motions transferred from external sources.",
    featured: {
      src: "videos/cross_reacttment/1.mp4",
      title: "Representative cross-reenactment sequence",
      subtitle: "Qualitative sequence"
    },
    items: Array.from({ length: 4 }, (_, index) => ({
      src: `videos/cross_reacttment/${index + 1}.mp4`,
      title: `Cross Reenactment ${index + 1}`,
      subtitle: "Qualitative sequence"
    }))
  },
  multiview: {
    overline: "View consistency",
    title: "Multi-View Consistency",
    description:
      "Multi-view sequences illustrating viewpoint consistency and appearance stability across rendered camera changes.",
    featured: {
      src: "videos/multiview/1.mp4",
      title: "Representative multi-view sequence",
      subtitle: "Qualitative sequence"
    },
    items: Array.from({ length: 9 }, (_, index) => ({
      src: `videos/multiview/${index + 1}.mp4`,
      title: `Multi-View ${index + 1}`,
      subtitle: "Qualitative sequence"
    }))
  }
};

let activeGroupKey = "self";

function createVideoCard(item) {
  return `
    <article class="video-card">
      <video controls muted playsinline preload="metadata">
        <source src="${item.src}" type="video/mp4">
      </video>
      <div class="video-meta">
        <strong>${item.title}</strong>
        <span>${item.subtitle}</span>
      </div>
    </article>
  `;
}

function renderFeaturedCard(group) {
  const container = document.getElementById("results-featured");

  if (!container) {
    return;
  }

  container.innerHTML = `
    <video class="featured-video" controls muted playsinline preload="metadata">
      <source src="${group.featured.src}" type="video/mp4">
    </video>
    <h3>${group.featured.title}</h3>
    <p>${group.featured.subtitle}</p>
  `;
}

function renderGallery(group) {
  const gallery = document.getElementById("results-gallery");

  if (!gallery) {
    return;
  }

  gallery.innerHTML = group.items.map(createVideoCard).join("");
}

function renderGroupCopy(group) {
  const overline = document.getElementById("results-group-overline");
  const title = document.getElementById("results-group-title");
  const description = document.getElementById("results-group-description");

  if (overline) {
    overline.textContent = group.overline;
  }

  if (title) {
    title.textContent = group.title;
  }

  if (description) {
    description.textContent = group.description;
  }
}

function syncFilterState() {
  const buttons = document.querySelectorAll(".results-filter-button");

  buttons.forEach((button) => {
    const isActive = button.dataset.group === activeGroupKey;
    button.classList.toggle("is-active", isActive);
    button.setAttribute("aria-selected", String(isActive));
  });
}

function renderCounts() {
  const totalClips = Object.values(resultGroups).reduce(
    (sum, group) => sum + group.items.length,
    0
  );
  const totalElement = document.getElementById("total-clips");

  if (totalElement) {
    totalElement.textContent = String(totalClips);
  }

  Object.entries(resultGroups).forEach(([groupKey, group]) => {
    const countElement = document.getElementById(`filter-count-${groupKey}`);

    if (countElement) {
      countElement.textContent = `${group.items.length} clips`;
    }
  });
}

function renderActiveResultsGroup() {
  const group = resultGroups[activeGroupKey];

  if (!group) {
    return;
  }

  renderFeaturedCard(group);
  renderGroupCopy(group);
  renderGallery(group);
  syncFilterState();
}

function bindResultFilters() {
  document.querySelectorAll(".results-filter-button").forEach((button) => {
    button.addEventListener("click", () => {
      const { group } = button.dataset;

      if (!group || group === activeGroupKey || !(group in resultGroups)) {
        return;
      }

      activeGroupKey = group;
      renderActiveResultsGroup();
    });
  });
}

function setCopyButtonState(button, label) {
  const copyText = button.querySelector(".copy-text");
  button.classList.add("copied");

  if (copyText) {
    copyText.textContent = label;
  }

  setTimeout(() => {
    button.classList.remove("copied");

    if (copyText) {
      copyText.textContent = "Copy";
    }
  }, 1800);
}

function fallbackCopy(payload, button) {
  const textArea = document.createElement("textarea");
  textArea.value = payload;
  textArea.setAttribute("readonly", "");
  textArea.style.position = "absolute";
  textArea.style.left = "-9999px";
  document.body.appendChild(textArea);
  textArea.select();
  document.execCommand("copy");
  document.body.removeChild(textArea);
  setCopyButtonState(button, "Copied");
}

function copyBibTeX() {
  const bibtexElement = document.getElementById("bibtex-code");
  const button = document.querySelector(".copy-bibtex-btn");

  if (!bibtexElement || !button) {
    return;
  }

  const payload = bibtexElement.textContent;

  if (navigator.clipboard && window.isSecureContext) {
    navigator.clipboard
      .writeText(payload)
      .then(() => {
        setCopyButtonState(button, "Copied");
      })
      .catch(() => {
        fallbackCopy(payload, button);
      });
    return;
  }

  fallbackCopy(payload, button);
}

function scrollToTop() {
  window.scrollTo({ top: 0, behavior: "smooth" });
}

window.addEventListener("scroll", () => {
  const button = document.querySelector(".scroll-to-top");

  if (!button) {
    return;
  }

  if (window.scrollY > 360) {
    button.classList.add("visible");
  } else {
    button.classList.remove("visible");
  }
});

document.addEventListener("DOMContentLoaded", () => {
  renderCounts();
  bindResultFilters();
  renderActiveResultsGroup();
});
