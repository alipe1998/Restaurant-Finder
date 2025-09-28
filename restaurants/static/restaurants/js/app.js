const configEl = document.getElementById('restaurant-config');
const appConfig = configEl ? JSON.parse(configEl.textContent) : {};

const state = {
  map: null,
  markers: [],
  infoWindow: null,
  results: [],
  initialized: false,
};

function updateRatingDisplay(value) {
  const output = document.getElementById('rating-display');
  if (output) {
    output.textContent = `${value}+`;
  }
}

function buildQueryFromForm(form) {
  const params = new URLSearchParams();
  const cuisineSelect = form.querySelector('#cuisine-select');
  if (cuisineSelect) {
    const selected = Array.from(cuisineSelect.selectedOptions).map((option) => option.value);
    if (selected.length) {
      params.set('cuisine', selected.join(','));
    }
  }

  const price = form.querySelector('input[name="price"]:checked');
  if (price && price.value) {
    params.set('price', price.value);
  }

  const rating = form.querySelector('#rating-min');
  if (rating && Number(rating.value) > 0) {
    params.set('rating_min', rating.value);
  }

  const openNow = form.querySelector('input[name="open_now"]');
  if (openNow && openNow.checked) {
    params.set('open_now', 'true');
  }

  return params;
}

function clearMarkers() {
  state.markers.forEach((marker) => marker.setMap(null));
  state.markers = [];
}

function createMarker(restaurant) {
  if (!state.map || typeof google === 'undefined') {
    return null;
  }

  const marker = new google.maps.Marker({
    position: { lat: restaurant.latitude, lng: restaurant.longitude },
    map: state.map,
    title: restaurant.name,
  });

  marker.addListener('click', () => {
    highlightCard(restaurant.id);
    if (!state.infoWindow) {
      state.infoWindow = new google.maps.InfoWindow();
    }
    state.infoWindow.setContent(`
      <div class="info-window">
        <strong>${restaurant.name}</strong><br />
        ${restaurant.cuisine} · ${restaurant.price_symbols}<br />
        Rating ${restaurant.average_rating.toFixed(1)} · ${restaurant.status_text}
      </div>
    `);
    state.infoWindow.open({ anchor: marker, map: state.map, shouldFocus: false });
  });

  return marker;
}

function highlightCard(id) {
  const list = document.getElementById('restaurants-list');
  if (!list) return;
  Array.from(list.children).forEach((item) => {
    const isActive = Number(item.dataset.id) === Number(id);
    item.dataset.active = isActive ? 'true' : 'false';
    if (isActive) {
      item.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }
  });
}

function renderList(restaurants) {
  const list = document.getElementById('restaurants-list');
  const count = document.getElementById('results-count');
  if (!list || !count) return;

  list.innerHTML = '';
  count.textContent = restaurants.length
    ? `${restaurants.length} restaurant${restaurants.length === 1 ? '' : 's'} found`
    : 'No restaurants match those filters yet.';

  restaurants.forEach((restaurant) => {
    const item = document.createElement('li');
    item.className = 'restaurant-card';
    item.dataset.id = restaurant.id;
    item.dataset.active = 'false';
    item.innerHTML = `
      <h3 class="restaurant-name">${restaurant.name}</h3>
      <div class="restaurant-meta">
        <span>${restaurant.cuisine}</span>
        <span>${restaurant.price_symbols}</span>
        <span>${restaurant.average_rating.toFixed(1)} ★</span>
        <span>${restaurant.status_text}</span>
      </div>
      <p class="restaurant-description">${restaurant.short_description}</p>
      <div class="restaurant-actions">
        <span>${restaurant.address}</span>
        ${restaurant.phone ? `<a href="tel:${restaurant.phone}">${restaurant.phone}</a>` : ''}
        ${restaurant.website ? `<a href="${restaurant.website}" target="_blank" rel="noopener">Website</a>` : ''}
      </div>
    `;
    item.addEventListener('mouseenter', () => highlightMarker(restaurant.id));
    list.appendChild(item);
  });
}

function highlightMarker(id) {
  state.markers.forEach((marker) => {
    const isActive = marker.__restaurantId === id;
    marker.setAnimation(isActive ? google.maps.Animation.DROP : null);
  });
  highlightCard(id);
}

async function fetchRestaurants(params) {
  const url = new URL(appConfig.apiBaseUrl, window.location.origin);
  url.search = params.toString();

  const response = await fetch(url.toString());
  if (!response.ok) {
    throw new Error('Failed to fetch restaurants');
  }
  const payload = await response.json();
  return payload.results.map((restaurant) => ({
    ...restaurant,
    latitude: Number(restaurant.latitude),
    longitude: Number(restaurant.longitude),
    average_rating: Number(restaurant.average_rating),
  }));
}

async function refreshRestaurants() {
  const form = document.getElementById('filters-form');
  if (!form) return;

  const params = buildQueryFromForm(form);
  try {
    const restaurants = await fetchRestaurants(params);
    state.results = restaurants;
    renderList(restaurants);
    clearMarkers();
    restaurants.forEach((restaurant) => {
      const marker = createMarker(restaurant);
      if (marker) {
        marker.__restaurantId = restaurant.id;
        state.markers.push(marker);
      }
    });
  } catch (error) {
    console.error(error);
    const count = document.getElementById('results-count');
    if (count) {
      count.textContent = 'We hit a snag loading restaurants.';
    }
  }
}

function attachFormListeners() {
  const form = document.getElementById('filters-form');
  if (!form) return;

  form.addEventListener('change', () => refreshRestaurants());

  const rating = form.querySelector('#rating-min');
  if (rating) {
    rating.addEventListener('input', (event) => {
      updateRatingDisplay(event.target.value);
    });
  }
}

function initMap() {
  if (typeof google === 'undefined' || !google.maps) {
    console.warn('Google Maps failed to load; falling back to list only experience.');
    return;
  }

  const center = appConfig.mapCenter || { lat: 30.2672, lng: -97.7431 };
  state.map = new google.maps.Map(document.getElementById('map'), {
    center,
    zoom: 13,
    mapId: 'restaurant-finder-map',
  });
}

function bootstrapApp() {
  if (state.initialized) {
    return;
  }
  state.initialized = true;
  attachFormListeners();
  const form = document.getElementById('filters-form');
  if (form) {
    const rating = form.querySelector('#rating-min');
    if (rating) {
      updateRatingDisplay(rating.value);
    }
  }
  refreshRestaurants();
}

window.initRestaurantFinder = function initRestaurantFinder() {
  bootstrapApp();
  initMap();
};

if (document.readyState === 'complete' || document.readyState === 'interactive') {
  bootstrapApp();
} else {
  document.addEventListener('DOMContentLoaded', bootstrapApp);
}
