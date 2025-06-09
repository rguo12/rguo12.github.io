---
permalink: /
title: about
author_profile: true
redirect_from: 
  - /about/
  - /about.html
---

Ruocheng Guo is a Staff Research Scientist at Intuit AI Research. His current research focus is LLM Agents, he also work on LLM reasoning, causal machine learning, and uncertainty quantification. Prior to joining Intuit, he was a Researcher at TikTok/ByteDance Research (London) and an Assistant Professor at City University of Hong Kong. He earned his Ph.D. degree from the Data Mining and Machine Learning Laboratory (DMML) at Arizona State University, advised by [Huan Liu](https://search.asu.edu/profile/255975), MSc degree from the beautiful HKUST and BEng degree from HUST.

Research Interests:
- LLMs (Agents, Dialogue, and Tool Use)
- Causal ML
- Recommendation Systems
- Data Mining

News
- 05/25 Got 2 papers in IJCAI'25, 1 paper in ACL'25, and 1 paper in KDD'25
- 03/25 Joined Intuit AI Research as a Staff Research Scientist
- Gave a talk at LinkedIn Market AI on LLM Agents [slides](), thank Dr. Liangjie Hong for the invitation
- 11/24 Invited to serve as PC co-chair of the industry track of IEEE DSAA'25
- 11/24 Invited by Dr. Jing Ma to give a guest lecture on conformal causal inference at Case Western Reserve University [slides]() 
- 10/24 A paper accepted to NeurIPS'24
- 08/24 Invited to present at [2nd Workshop on Causal Inference and Machine Learning in Practice @ KDD'24](https://causal-machine-learning.github.io/kdd2024-workshop/)

Interested in Causal ML? Please find our papers and algorithm/data repositories.
- Survey Papers
  - [Causal Interpretability for Machine Learning--Problems, Methods and Evaluation](https://arxiv.org/pdf/2003.03934.pdf)
  - [A Survey of Learning Causality with Data: Problems and Methods](https://arxiv.org/pdf/1809.09337)
- Repositories
  - Algorithm Repository: [Awesome-Causality-Algorithms](https://github.com/rguo12/awesome-causality-algorithms)
  - Data Repository: [Awesome-Causality-Data](https://github.com/rguo12/awesome-causality-data)


Experience:
- Staff Research Scientist, [Intuit AI Research](https://www.intuit.com/ai/research/), March 2025 - 
- Senior Machine Learning Researcher, ByteDance Research, June 2022 - Jan 2025
- Assistant Professor, City University of Hong Kong, Aug 2021 - June 2022
- AI Resident, Google X, Aug 2020 - Dec 2020
  - Mentor: Hongxu Ma
- Research Intern, Microsoft Research, May 2020 - Aug 2020
  - Mentor: [Emre Kiciman](https://kiciman.org/), [Pengchuan Zhang](https://pzzhang.github.io/pzzhang/)
- Research Intern, Etsy, May 2019 - Aug 2019
  - Mentor: [Liangjie Hong](https://www.hongliangjie.com/), Xiaoting Zhao, Adam Henderson

Students and Interns (and papers co-authored with me)
- [Maolin Wang](https://morin.wang/) (PhD Student@City University of Hong Kong, Co-supervised w. Xiangyu Zhao and Junhui Wang)
  - ACL'25, KDD'25, SIGIR'25, IJCAI'25, WWW'24, SDM'24, ICDM'23
- [Zonghao Chen](https://hudsonchen.github.io/) (PhD Student@UCL, Intern@ByteDance Research)
  - KDD'24
- Tongxin Yin (PhD Student@UMich, Intern@ByteDance Research)
  - ICLR'24
- Qing Zhang (PhD Student@HKUST, Intern@ByteDance Research)
  - KDD'23
- Xiaohui Chen (PhD Student@Tufts, Intern@ByteDance)
  - KDD'23
- Chentao Cao (PhD Student@HKBU, Intern@ByteDance Research)
- Sichun Luo (PhD Student@CityU, Intern@ByteDance)
- Xinjian Zhao (Master Student@CityU -> PhD Student@CUHK SZ)
- Jiansheng Li (Master Student@CityU -> PhD Student@CUHK SZ)

## Visitor Map

<div style="margin-top: 30px; padding: 20px; background: #f8f9fa; border-radius: 8px; border: 1px solid #dee2e6;">
  <h3 style="margin-top: 0; color: #495057; text-align: center;">🌍 Website Visitors</h3>
  <div id="about-visitor-map" style="height: 300px; width: 100%; border-radius: 6px; margin: 15px 0;"></div>
  <div style="text-align: center; font-size: 14px; color: #666;">
    <span id="about-total-visitors">0</span> visitors from <span id="about-unique-countries">0</span> countries
  </div>
</div>

<!-- Leaflet CSS -->
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.7.1/dist/leaflet.css" />

<script src="https://unpkg.com/leaflet@1.7.1/dist/leaflet.js"></script>
<script>
(function() {
  'use strict';
  
  const STORAGE_KEY = 'geolocation_stats';
  const VISITOR_KEY = 'visitor_tracked';
  
  let aboutMap = null;
  let geolocationData = JSON.parse(localStorage.getItem(STORAGE_KEY)) || {
    totalVisitors: 0,
    countries: {},
    visitors: [],
    lastUpdated: Date.now()
  };
  
  // Initialize the about page map
  function initializeAboutMap() {
    if (aboutMap) {
      aboutMap.remove();
    }
    
    aboutMap = L.map('about-visitor-map', {
      zoomControl: true,
      attributionControl: false
    }).setView([20, 0], 2);
    
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      maxZoom: 10,
      minZoom: 1
    }).addTo(aboutMap);
    
    // Add existing visitor markers
    geolocationData.visitors.forEach((visitor, index) => {
      addMarkerToAboutMap(visitor.lat, visitor.lng, visitor.city, visitor.country, visitor.timestamp);
    });
    
    // Fit map to show all markers if there are any
    if (geolocationData.visitors.length > 0) {
      const group = new L.featureGroup(geolocationData.visitors.map(v => L.marker([v.lat, v.lng])));
      aboutMap.fitBounds(group.getBounds().pad(0.1));
    }
  }
  
  // Add marker to about page map
  function addMarkerToAboutMap(lat, lng, city, country, timestamp) {
    if (!aboutMap) return;
    
    const marker = L.circleMarker([lat, lng], {
      radius: 8,
      fillColor: '#ff7800',
      color: '#fff',
      weight: 2,
      opacity: 1,
      fillOpacity: 0.8
    }).addTo(aboutMap);
    
    const date = new Date(timestamp).toLocaleDateString();
    marker.bindPopup(`<b>${city}, ${country}</b><br/>Visited: ${date}`);
  }
  
  // Update display
  function updateAboutDisplay() {
    document.getElementById('about-total-visitors').textContent = geolocationData.totalVisitors;
    document.getElementById('about-unique-countries').textContent = Object.keys(geolocationData.countries).length;
  }
  
  // Track visitor (same as before)
  function trackVisitor() {
    if (sessionStorage.getItem(VISITOR_KEY)) {
      updateAboutDisplay();
      return;
    }
    
    fetch('https://ipapi.co/json/')
      .then(response => response.json())
      .then(data => {
        const country = data.country_name || 'Unknown';
        const city = data.city || 'Unknown';
        const lat = data.latitude || 0;
        const lng = data.longitude || 0;
        
        geolocationData.totalVisitors++;
        geolocationData.countries[country] = (geolocationData.countries[country] || 0) + 1;
        
        if (lat && lng) {
          const newVisitor = {
            lat: lat,
            lng: lng,
            city: city,
            country: country,
            timestamp: Date.now()
          };
          
          geolocationData.visitors.push(newVisitor);
          
          if (geolocationData.visitors.length > 50) {
            geolocationData.visitors = geolocationData.visitors.slice(-50);
          }
          
          addMarkerToAboutMap(lat, lng, city, country, newVisitor.timestamp);
        }
        
        geolocationData.lastUpdated = Date.now();
        localStorage.setItem(STORAGE_KEY, JSON.stringify(geolocationData));
        sessionStorage.setItem(VISITOR_KEY, 'true');
        
        updateAboutDisplay();
      })
      .catch(err => {
        console.log('Primary IP geolocation failed, trying backup:', err);
        fetch('https://api.bigdatacloud.net/data/ip-geolocation?key=&ip=')
          .then(response => response.json())
          .then(data => {
            const country = data.country?.name || 'Unknown';
            const city = data.location?.city || 'Unknown';
            const lat = data.location?.latitude || 0;
            const lng = data.location?.longitude || 0;
            
            geolocationData.totalVisitors++;
            geolocationData.countries[country] = (geolocationData.countries[country] || 0) + 1;
            
            if (lat && lng) {
              const newVisitor = {
                lat: lat,
                lng: lng,
                city: city,
                country: country,
                timestamp: Date.now()
              };
              
              geolocationData.visitors.push(newVisitor);
              
              if (geolocationData.visitors.length > 50) {
                geolocationData.visitors = geolocationData.visitors.slice(-50);
              }
              
              addMarkerToAboutMap(lat, lng, city, country, newVisitor.timestamp);
            }
            
            geolocationData.lastUpdated = Date.now();
            localStorage.setItem(STORAGE_KEY, JSON.stringify(geolocationData));
            sessionStorage.setItem(VISITOR_KEY, 'true');
            
            updateAboutDisplay();
          })
          .catch(backupErr => {
            console.log('Backup geolocation also failed:', backupErr);
            geolocationData.totalVisitors++;
            geolocationData.countries['Unknown'] = (geolocationData.countries['Unknown'] || 0) + 1;
            geolocationData.lastUpdated = Date.now();
            
            localStorage.setItem(STORAGE_KEY, JSON.stringify(geolocationData));
            sessionStorage.setItem(VISITOR_KEY, 'true');
            
            updateAboutDisplay();
          });
      });
  }
  
  // Initialize everything
  updateAboutDisplay();
  
  // Initialize map when page loads
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function() {
      setTimeout(initializeAboutMap, 500);
      setTimeout(trackVisitor, 1000);
    });
  } else {
    setTimeout(initializeAboutMap, 500);
    setTimeout(trackVisitor, 1000);
  }
  
  // Clean up old data
  if (Date.now() - geolocationData.lastUpdated > 30 * 24 * 60 * 60 * 1000) {
    geolocationData = {
      totalVisitors: 0,
      countries: {},
      visitors: [],
      lastUpdated: Date.now()
    };
    localStorage.setItem(STORAGE_KEY, JSON.stringify(geolocationData));
  }
})();
</script>

