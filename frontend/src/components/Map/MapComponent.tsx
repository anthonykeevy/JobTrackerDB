import React, { useRef, useEffect } from 'react';
import mapboxgl from 'mapbox-gl';
import 'mapbox-gl/dist/mapbox-gl.css';

// Mapbox access token - in production, use environment variable
const MAPBOX_TOKEN = import.meta.env?.VITE_MAPBOX_TOKEN || 'pk.eyJ1IjoiYW50aG9ueWtlZXZ5IiwiYSI6ImNtZHR1NXFjejBhdTkybW9qdmJoenZxNWoifQ.eKJynTPhNLEd4TrbUY2aNA';

interface MapComponentProps {
  latitude: number;
  longitude: number;
  address?: string;
  className?: string;
}

const MapComponent: React.FC<MapComponentProps> = ({ 
  latitude, 
  longitude, 
  address, 
  className = "w-full h-64" 
}) => {
  const mapContainer = useRef<HTMLDivElement>(null);
  const map = useRef<mapboxgl.Map | null>(null);

  useEffect(() => {
    if (!mapContainer.current || !MAPBOX_TOKEN) return;

    if (map.current) return; // Initialize map only once

    map.current = new mapboxgl.Map({
      container: mapContainer.current,
      style: 'mapbox://styles/mapbox/streets-v11',
      center: [longitude, latitude],
      zoom: 15,
      accessToken: MAPBOX_TOKEN
    });

    // Add marker
    new mapboxgl.Marker()
      .setLngLat([longitude, latitude])
      .addTo(map.current);

    // Add popup with address
    if (address) {
      new mapboxgl.Popup({ offset: 25 })
        .setLngLat([longitude, latitude])
        .setHTML(`<div class="text-sm font-medium">${address}</div>`)
        .addTo(map.current);
    }

    return () => {
      if (map.current) {
        map.current.remove();
        map.current = null;
      }
    };
  }, [latitude, longitude, address]);

  // Fallback component when Mapbox token is not available
  if (!MAPBOX_TOKEN) {
    return (
      <div className={`${className} bg-gray-100 rounded-lg border border-gray-300 relative overflow-hidden`}>
        <div className="absolute inset-0 flex items-center justify-center text-gray-500">
          <div className="text-center">
            <div className="w-8 h-8 mx-auto mb-2 text-blue-600">
              <svg fill="currentColor" viewBox="0 0 24 24">
                <path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z"/>
              </svg>
            </div>
            <p className="text-sm font-medium">Address Location</p>
            <p className="text-xs text-gray-400 mt-1">
              Lat: {latitude.toFixed(4)}, Lng: {longitude.toFixed(4)}
            </p>
            {address && (
              <p className="text-xs text-gray-600 mt-2 max-w-xs">
                {address}
              </p>
            )}
            <p className="text-xs text-gray-400 mt-3">
              Map requires Mapbox API key
            </p>
          </div>
        </div>
      </div>
    );
  }

  return <div ref={mapContainer} className={className} />;
};

export default MapComponent;