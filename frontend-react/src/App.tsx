import { useState, useCallback } from 'react'
import './App.css'
import 'katex/dist/katex.min.css'
import { BlockMath } from 'react-katex'

interface TikTokResponseUI {
  reward_score: number
  thumbnail: {
    local_path: string
    url: string
  },
  engagement_index: {
    EVI: number
    components: {
      likes_ratio: number
      shares_ratio: number
      comments_ratio: number
      collect_ratio: number
    }
  }
  content_quality: {
    positivity_rate: number
    toxicity_rate: number
    Mquality: number
  }
  aigc_integrity: {
    probability_aigc: number
    Mintegrity: number
  }
  mission_bonus: {
    small_creator: boolean
    underrepresented_country: boolean
    Bmission: number
  }
}

export function App() {
  const [videoUrl, setVideoUrl] = useState('')
  const [result, setResult] = useState<TikTokResponseUI | null>(null)
  const [loading, setLoading] = useState(false)
  const [showInfo, setShowInfo] = useState<{ [key: string]: boolean }>({})

  const toggleInfo = (key: string) => {
    setShowInfo((prev) => ({ ...prev, [key]: !prev[key] }))
  }

  const onAnalyze = useCallback(async () => {
    if (!videoUrl.trim()) return alert('Please enter a TikTok URL')
    setLoading(true)
    setResult(null)

    try {
      const res = await fetch('http://localhost:8000/analyse_tiktok', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ video_url: videoUrl }),
      })
      const data = await res.json()
      setResult(data)
    } catch (err) {
      console.error(err)
      alert(err)
    } finally {
      setLoading(false)
    }
  }, [videoUrl])

  return (
    <div className="App">
      <h1 style={{
        fontFamily: 'Arial, sans-serif',
        color: '#FF0050',
        textAlign: 'center',
        lineHeight: 1.3
      }}>
        BrightShare<br />
        <span style={{ fontSize: '0.6em', color: '#555' }}>
          Fair, Transparent, and Inclusive Rewards for TikTok Creators
        </span>
      </h1>

      <h2>
        What's the Reward for this TikTok?
      </h2>

      <input
        type="text"
        placeholder="Enter TikTok video URL"
        value={videoUrl}
        onChange={(e) => setVideoUrl(e.target.value)}
        className="Input"
      />

      <button
        onClick={onAnalyze}
        className="AnalyzeButton"
        disabled={loading}
      >
        {loading ? 'Analyzing…' : 'Analyze'}
      </button>

      {result && (
        <div className="ResultCard">
          {/* Value Score */}
          <div className="CompositeScore">
            <span className="MetricLabel">
              Reward Score
            <button className="InfoButton" onClick={() => toggleInfo('composite_score')}>i</button>
            </span>
            <div className="ScoreNumber">{result.reward_score.toFixed(2)}</div>
            {showInfo['composite_score'] && (
            <div className="InfoBox show">
                Overall value score combining engagement, community quality, AIGC integrity, and inclusivity index.
              <BlockMath math="\text{Reward} = R_{\text{base}} \times M_{\text{quality}} \times M_{\text{integrity}} \times I_{\text{index}}" />

              <p><strong>Base Reward:</strong></p>
              <BlockMath math="R_{\text{base}} = \text{Ad Revenue from TikTok} + \text{Gifted (Stickers)} + \text{Engagement Value Index (EVI)}" />
            </div>
          )}
          </div>
          {/*           
          {result.thumbnail?.local_path && (
            <div style={{ marginBottom: '2rem' }}>
              <img
                src={result.thumbnail.url || result.thumbnail.local_path}
                alt={result.thumbnail.url}
                style={{ maxWidth: '300px', width: '100%', borderRadius: '12px' }}
              />
            </div>
          )} */}
    
          {/* Two columns */}
          <div className="Columns">
            {/* Left Column */}
            <div className="Column">
              {/* Engagement Index */}
              <div className="MetricCard">
                <span className="MetricLabel">
                  Engagement Value Index
                  <button className="InfoButton" onClick={() => toggleInfo('engagement')}>i</button>
                </span>
                <div className="MetricValue">
                    {result.engagement_index.EVI.toFixed(5)} <br />
                </div>
                <div className="MetricSubValue">
                  Likes Ratio: {(result.engagement_index.components.likes_ratio).toFixed(4)}<br/>
                  Shares Ratio: {(result.engagement_index.components.shares_ratio).toFixed(4)}<br/>
                  Comments Ratio: {(result.engagement_index.components.comments_ratio).toFixed(4)}<br/>
                  Collects Ratio: {(result.engagement_index.components.collect_ratio).toFixed(4)}
                </div>
                {showInfo['engagement'] && (
                  <div className="InfoBox show">
                    Measures user interaction related ratio metrics including likes, shares, comments, and collects.
                  <p><strong>Engagement Value Index (EVI):</strong></p>
                  <BlockMath math="\text{EVI} = 0.1 \frac{\text{Likes}}{\text{Views}} + 0.4 \frac{\text{Shares}}{\text{Views}} + 0.3 \frac{\text{Comments}}{\text{Views}} + 0.2 \frac{\text{Collects}}{\text{Views}}" />
                  </div>
                )}
              </div>

              {/* Content Quality */}
              <div className="MetricCard">
                <span className="MetricLabel">
                  Community & Content Quality
                  <button className="InfoButton" onClick={() => toggleInfo('content')}>i</button>
                </span>
                <div className='MetricValue'>
                  {result.content_quality.Mquality.toFixed(2)}
                </div>
                <div className="MetricSubValue">
                  Positivity Score: {(result.content_quality.positivity_rate).toFixed(4)} <br/>
                  Toxicity Score: {(result.content_quality.toxicity_rate).toFixed(4)} <br/>
                </div>
                {showInfo['content'] && (
                  <div className="InfoBox show">
                    Analyzes the positivity & toxicity of the video's comment section via NLP sentiment analysis.
                    <p><strong>Community & Content Quality Multiplier:</strong></p>
                  <BlockMath math="M_{\text{quality}} = 0.5 \times \text{Positivity Rate} + 0.5 \times \text{1- Toxicity Rate}" />
              <p>where Positivity Rate and Toxicity Rate are determined using a pre-trained Twitter RoBERTa model and Google Perspective</p>
                  </div>
                )}
              </div>
            </div>

            {/* Right Column */}
            <div className="Column">
              {/* AIGC Integrity */}
              <div className="MetricCard">
                <span className="MetricLabel">
                  AIGC Integrity
                  <button className="InfoButton" onClick={() => toggleInfo('aigc')}>i</button>
                </span>
                <div className='MetricValue'>
                 {result.aigc_integrity.Mintegrity.toFixed(3)}
                </div>
                <div className="MetricSubValue">
                  AIGC Probability: {(result.aigc_integrity.probability_aigc*100).toFixed(1)}% <br/>
                </div>
                {showInfo['aigc'] && (
                  <div className="InfoBox show">
                    Probability that content is AI-generated.
                                      <p><strong>AIGC Integrity Multiplier:</strong></p>
              <BlockMath math="M_{\text{integrity}} = 1 - 0.25 \times \min\big(1, \text{Probability of AIGC}\big)" />


                  </div>
                )}
              </div>

              {/* Mission Bonus */}
              <div className="MetricCard">
                <span className="MetricLabel">
                  Inclusivity Bonus
                  <button className="InfoButton" onClick={() => toggleInfo('mission')}>i</button>
                </span>
                <div className='MetricValue'>
                 {result.mission_bonus.Bmission.toFixed(2)}
                </div>
                <div className="MetricSubValue">
                  Small Creator: {result.mission_bonus.small_creator ? 'Yes' : 'No'} <br/>
                  Underrepresented Country: {result.mission_bonus.underrepresented_country ? 'Yes' : 'No'} <br/>
                </div>
                {showInfo['mission'] && (
                  <div className="InfoBox show">
                    Extra reward for small creators or creators from underrepresented countries.
                    <p><strong>Inclusivity Index:</strong></p>
              <BlockMath math="I_{\text{index}} = \bigg( 1 + 0.1 \cdot \mathbf{1}_{\text{Small Creator}} + 0.1 \cdot \mathbf{1}_{\text{Underrepresented Community}} \bigg)" />
                            <BlockMath math="\mathbf{1}_{\text{Small Creator}} =
              \begin{cases}
              1, & \text{if followers} < \text{threshold} \\
              0, & \text{otherwise}
              \end{cases}" />
              
              <BlockMath math="\mathbf{1}_{\text{Underrepresented Community}} =
              \begin{cases}
              1, & \text{if country in TikTok expansion list} \\
              0, & \text{otherwise}
              \end{cases}" />
                  </div>
                  
                )}
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
