import React from 'react';
import { ProductRecommendation } from '../../services/api';

interface ProductCardProps {
  products: ProductRecommendation[];
}

export const ProductCard: React.FC<ProductCardProps> = ({ products }) => {
  return (
    <div className="product-section">
      <h3 className="section-title">
        🎯 <span>맞춤형 3대 추천 상품군</span>
      </h3>
      <div className="product-grid">
        {(products || []).map((prod) => (
          <div key={prod.id} className="product-card">
            <div className="product-card-header">
              <span className="product-category">{prod.category}</span>
              <span className="product-tag">{prod.tag}</span>
            </div>
            <h4 className="product-name">
              {prod.name}
              {prod.is_live && <span className="live-badge">🟢 실시간</span>}
            </h4>
            <p className="product-desc">{prod.description}</p>
            {prod.items && prod.items.length > 0 && (
              <div className="product-items">
                <div className="item-label">대표 혜택 & 가이드:</div>
                <ul className="item-list">
                  {prod.items.map((item, i) => (
                    <li key={i}>• {item}</li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
};
