import React, { useRef, useEffect } from 'react';
import mapboxgl from 'mapbox-gl';
import 'mapbox-gl/dist/mapbox-gl.css';

// Mapbox access token - in production, use environment variable
const MAPBOX_TOKEN = import.meta.env?.VITE_MAPBOX_TOKEN || 'pk.eyJ1IjoiYW50aG9ueWtlZXZ5IiwiYSI6ImNtZHR1NXFjejBhdTkybW9qdmJoenZxNWoifQ.eKJynTPhNLEd4TrbUY2aNA';

// Note: Chrome may show WebGL warnings (crbug.com/24299) - this is a known Chrome issue
// and doesn't affect map functionality. Maps will automatically fall back to software rendering.

interface MapComponentProps {
  latitude?: number;
  longitude?: number;
  address?: string;
  className?: string;
}

const MapComponent: React.FC<MapComponentProps> = ({ 
  latitude, 
  longitude, 
  address, 
  className = "" 
}) => {
  const mapContainer = useRef<HTMLDivElement>(null);
  const map = useRef<mapboxgl.Map | null>(null);

  // Only render map if we have valid coordinates
  const hasValidCoordinates = latitude && longitude && 
    typeof latitude === 'number' && typeof longitude === 'number' &&
    !isNaN(latitude) && !isNaN(longitude) &&
    latitude !== 0 && longitude !== 0;

  useEffect(() => {
    if (!mapContainer.current || !hasValidCoordinates) {
      return;
    }

    // Initialize map only if we have valid coordinates
    if (!map.current) {
      mapboxgl.accessToken = MAPBOX_TOKEN;
      
      map.current = new mapboxgl.Map({
        container: mapContainer.current,
        style: 'mapbox://styles/mapbox/streets-v12',
        center: [longitude, latitude],
        zoom: 15
      });

      // Add navigation controls
      map.current.addControl(new mapboxgl.NavigationControl(), 'top-right');

      // Add marker for the address
      new mapboxgl.Marker()
        .setLngLat([longitude, latitude])
        .addTo(map.current);
    } else {
      // Update existing map
      map.current.setCenter([longitude, latitude]);
    }
  }, [latitude, longitude, hasValidCoordinates]);

  // Cleanup on unmount
  useEffect(() => {
    return () => {
      if (map.current) {
        map.current.remove();
        map.current = null;
      }
    };
  }, []);

  // Don't render anything if we don't have valid coordinates
  if (!hasValidCoordinates) {
    return null;
  }

  return (
    <div className={`w-full h-64 rounded-lg overflow-hidden border ${className}`}>
      <div ref={mapContainer} className="w-full h-full" />
    </div>
  );
};

export default MapComponent;