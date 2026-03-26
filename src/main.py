#!/usr/bin/env python3
"""
TravelPlanner - Social media travel research tool
"""
import argparse
from pathlib import Path

def main():
    parser = argparse.ArgumentParser(description='TravelPlanner')
    parser.add_argument('--destination', '-d', help='Destination to research')
    parser.add_argument('--platforms', '-p', default='all', help='Platforms to search')
    parser.add_argument('--output', '-o', default='data/saved', help='Output directory')
    
    args = parser.parse_args()
    
    print("🗺️ TravelPlanner")
    print(f"📍 Destination: {args.destination}")
    print(f"📱 Platforms: {args.platforms}")
    
    # TODO: Implement scrapers
    
if __name__ == '__main__':
    main()
